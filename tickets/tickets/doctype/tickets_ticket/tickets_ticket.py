# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils.data import format_datetime
from frappe.model.document import Document
from tickets.tickets.doctype.tickets_site.tickets_site import list_user_sites, list_admin_sites

class TicketsTicket(Document):
	def on_submit(self):
		task = frappe.get_doc("Tickets Task", self.task)
		task.append_tickets(self)
		if self.wechat_notify == 1:
			frappe.enqueue('tickets.tickets.doctype.tickets_ticket.tickets_ticket.wechat_notify_by_ticket_name',
							ticket_name = self.name, ticket_doc=self)

	def on_cancel(self):
		task = frappe.get_doc("Tickets Task", self.task)
		task.remove_tickets(self)

	def remove_all_reports(self):
		self.set("reports", list())

	def append_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted tickets"))

		current_reports = [d.report for d in self.get("reports")]
		for report in reports:
			if report.name in current_reports:
				continue
			self.append("reports", {"report": report.name})

		self.save()

	def remove_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted tickets"))

		existing_reports = dict((d.report, d) for d in self.get("reports"))
		for report in reports:
			if report.name in existing_reports:
				self.get("reports").remove(existing_reports[report.name])

		self.save()

	def update_cost(self):
		if self.docstatus == 2:
			return

		for d in self.get("items"):
			rate = self.get_bom_material_detail({'item_code': d.item_code, 'bom_no': d.bom_no,
				'qty': d.qty})["rate"]
			if rate:
				d.rate = rate

		if self.docstatus == 1:
			self.flags.ignore_validate_update_after_submit = True
			self.calculate_cost()
		self.save()
		self.update_exploded_items()

		frappe.msgprint(_("Cost Updated"))

	def ticket_get(self):
		if self.docstatus == 2:
			return
		if self.status != 'New':
			throw(_("Current tickets is not in new state"))

		if self.assigned_to_user and self.asigned_to_user != frappe.session.user:
			throw(_("This tickets is assigned to {1}").format(self.assigned_to_user))

		if self.site not in list_user_sites(frappe.session.user, self.task_type):
			throw(_("You have no permission to get this tickets"))

		self.assigned_to_user = frappe.session.user

		self.set('status', 'Fixing')
		self.save()

		frappe.msgprint(_("You Got This Ticket"))

	def ticket_fixed(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixing':
			throw(_("Current tickets is not in fixing state"))

		if self.assigned_to_user != frappe.session.user:
			throw(_("This tickets is assigned to {1}").format(self.assigned_to_user))
		self.set('status', 'Fixed')
		self.save()

		frappe.msgprint(_("Ticket Fixed"))

	def ticket_close(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixed':
			throw(_("Current tickets is not in fixed state"))

		self.set('status', 'Closed')
		self.save()

		frappe.msgprint(_("Ticket Closed"))

	def ticket_reject(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixed':
			throw(_("Current tickets is not in fixed state"))

		self.set('status', 'Rejected')
		self.save()

		frappe.msgprint(_("Ticket Fix Rejected"))

	def create_delivery_order(self):
		"""
		Create delivery order for this ticket
		:return: 
		"""
		if self.docstatus != 1:
			throw(_("Cannot create delivery order for un-commited oder!"))

		if self.delivery_order:
			throw(_("Delivery order already created!"))

		if not is_stock_installed():
			throw(_("Stock App is not installed"))

		items = []
		for item in self.get("items"):
			for i in range(0, item.qty):
				items.append({"item": item.item, "remark": item.remark})

		if len(items) == 0:
			throw(_("Cannot create delivery order as this ticket has no item list"))

		order = {
			"order_source_type": 'Tickets Ticket',
			"order_source_id": self.name,
			"naming_series": "TKT-",
			"doctype": "Stock Delivery Order",
			"items": items,
		}
		doc = frappe.get_doc(order).insert(ignore_permissions=True)

		doc.save()
		self.delivery_order = doc.name
		self.save()

		frappe.msgprint(doc.name)

	def on_delivery_order_cancel(self):
		self.delivery_order = None
		self.delivery_warehouse = None
		self.save()

	def on_delivery_order_commit(self, order):
		if self.delivery_order != order.name:
			return
		self.delivery_warehouse = order.warehouse
		self.save()

	def wechat_tmsg_data(self):
		return {
			"first": {
				"value": _("New Ticket Created"),
				"color": "red"
			},
			"keyword1": {
				"value": self.name,  # 编号
				"color": "blue"
			},
			"keyword2": {
				"value": self.ticket_name,  # 标题
				"color": "blue"
			},
			"keyword3": {
				"value": format_datetime(self.planned_end_date),  # 时间
				"color": "green",
			},
			"remark": {
				"value": _("Task: {0}\nPrice: {1}\nInfo: {2}").format(self.task, self.cost, self.info)
			}
		}

	def wechat_tmsg_url(self):
		return "/desk#Form/Tickets Ticket/" + self.name


def get_permission_query_conditions(user):
	if 'Tickets Manager' in frappe.get_roles(user):
		return ""

	sites = list_admin_sites(user)

	# [frappe.db.escape(r) for r in frappe.get_roles(user)]
	if len(sites) != 0:
		return """(`tabTickets Ticket`.site in ({sites}))""".format(
			sites='"' + '", "'.join(sites) + '"')

	return """(`tabTickets Ticket`.assigned_to_user = '{0}')""".format(user)


def wechat_notify_by_ticket_name(ticket_name, ticket_doc=None):
	from cloud.cloud.doctype.cloud_company.cloud_company import get_wechat_app
	from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_users

	ticket_doc = ticket_doc or frappe.get_doc("Tickets Ticket", ticket_name)

	user_list = {}
	# Get all teams for that site
	for st in frappe.db.get_values("Tickets SiteTeam", {"parent": ticket_doc.site, "type": ticket_doc.task_type}, "team"):
		app = get_wechat_app(frappe.db.get_value("Cloud Company Group", st[0], "company"))
		if app:
			if not user_list.has_key(app):
				user_list[app] = []
			for d in list_users(st[0]):
				user_list[app].append(d.name)
			"""
			frappe.sendmail(recipients=email_account.get_unreplied_notification_emails(),
				content=comm.content, subject=comm.subject, doctype= comm.reference_doctype,
				name=comm.reference_name)
			"""
	for app in user_list:
		#print("Send wechat notify : {0} to users {1} via app {2}".format(task_doc.as_json(), user_list[app], app))
		from wechat.api import send_doc
		send_doc(app, 'Tickets Ticket', ticket_doc.name, user_list[app])


@frappe.whitelist()
def is_stock_installed():
	return "tieta" in frappe.get_installed_apps()

