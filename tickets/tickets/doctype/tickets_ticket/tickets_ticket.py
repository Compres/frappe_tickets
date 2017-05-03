# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import getdate, nowdate
from frappe.utils.data import format_datetime
from frappe.model.document import Document


class TicketsTicket(Document):
	def validate(self):
		self.project = frappe.get_value(self.site_type, self.site, "project")
		if self.site_type == 'Cell Station':
			self.site_name = frappe.get_value(self.site_type, self.site, "station_name")
		if self.site_type == 'Cloud Project Site':
			self.site_name = frappe.get_value(self.site_type, self.site, "site_name")

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

		if not self.has_get_perm():
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

		self.set('actual_end_date', getdate(nowdate()))
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
			throw(_("Cannot create delivery order for un-commited ticket!"))

		if self.delivery_order:
			throw(_("Delivery order already created!"))

		if not is_stock_installed():
			throw(_("Stock App is not installed"))

		items = []
		for item in self.get("items"):
			if frappe.get_value("Stock Item", item.item, "has_serial_no") == 1:
				for i in range(0, item.qty):
					items.append({"item": item.item, "qty": 1, "remark": item.remark})
			else:
				items.append({"item": item.item, "qty": item.qty, "remark": item.remark})

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

	def __get_address_text(self):
		return frappe.get_value(self.site_type, self.site, "address_text")

	def get_region_address(self):
		region = frappe.get_value("Region Address", {"parent": self.site, "parenttype": self.site_type}, "name")
		return frappe.get_doc("Region Address", region)

	def has_get_perm(self, user=None):
		region = self.get_region_address()
		from tickets.tickets.doctype.tickets_region.tickets_region import list_user_regions
		list = list_user_regions(user or frappe.session.user)
		for d in list:
			if region.is_region_of(d):
				return True
		return False

	def wechat_tmsg_data(self):
		remark = _("Task: {0}").format(self.task) + "\n" + \
				_("Price: {0}").format(self.cost) + "\n" + \
				_("Address: {0}").format(self.__get_address_text())
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
				"value": remark
			}
		}

	def wechat_tmsg_url(self):
		return "/desk#Form/Tickets Ticket/" + self.name


def get_permission_query_conditions(user):
	if 'Tickets Manager' in frappe.get_roles(user):
		return ""

	from cloud.cloud.doctype.cloud_project.cloud_project import list_user_projects
	projects = list_user_projects(user)

	# [frappe.db.escape(r) for r in frappe.get_roles(user)]
	if len(projects) != 0:
		return """(`tabTickets Ticket`.assigned_to_user = "{user}" or `tabTickets Ticket`.project in ({projects}))""".format(
			user = user,
			projects='"' + '", "'.join(projects) + '"')

	return """(`tabTickets Ticket`.assigned_to_user = '{0}')""".format(user)


def get_users_by_region(user_list, region, ticket_doc):
	from cloud.cloud.doctype.cloud_company.cloud_company import get_wechat_app
	from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_users
	# Get all teams for that site
	for rgn in frappe.db.get_values("Tickets Region", {"region": region, "enabled": 1}, "name"):
		for st in frappe.db.get_values("Tickets RegionTeam", {"parent": rgn[0], "type": ticket_doc.task_type}, "team"):
			app = get_wechat_app(frappe.db.get_value("Cloud Company Group", st[0], "company"))
			if app:
				if not user_list.has_key(app):
					user_list[app] = []
				for d in list_users(st[0]):
					user_list[app].append(d.name)
	return user_list


def wechat_notify_by_ticket_name(ticket_name, ticket_doc=None):
	ticket_doc = ticket_doc or frappe.get_doc("Tickets Ticket", ticket_name)
	region = ticket_doc.get_region_address()

	user_list = {}
	user_list = get_users_by_region(user_list, region.town, ticket_doc)
	user_list = get_users_by_region(user_list, region.county, ticket_doc)
	user_list = get_users_by_region(user_list, region.city, ticket_doc)
	user_list = get_users_by_region(user_list, region.province, ticket_doc)

	for app in user_list:
		#print("Send wechat notify : {0} to users {1} via app {2}".format(task_doc.as_json(), user_list[app], app))
		from wechat.api import send_doc
		send_doc(app, 'Tickets Ticket', ticket_doc.name, user_list[app])


@frappe.whitelist()
def is_stock_installed():
	return "tieta" in frappe.get_installed_apps()


@frappe.whitelist()
def list_ticket_map():
	from cloud.cloud.doctype.cloud_project.cloud_project import list_user_projects
	projects = list_user_projects(frappe.session.user)
	if len(projects) == 0:
		return []
	tasks = frappe.get_all('Tickets Task', filters={"docstatus": ["in",[1, 2]], "project": ["in", projects]},
							fields=["name", "task_name", "site", "priority", "total_cost", "status"])

	for task in tasks:
		task.longitude = frappe.get_value(task.site_type, task.site, "longitude") or '116.3252'
		task.latitude = frappe.get_value(task.site_type, task.site, "latitude") or '40.045103'
	return tasks
