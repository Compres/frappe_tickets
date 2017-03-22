# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils.data import format_datetime
from frappe.model.document import Document
from repair.repair.doctype.repair_site.repair_site import list_sites

class RepairTicket(Document):
	def on_submit(self):
		issue = frappe.get_doc("Repair Issue", self.issue)
		issue.append_tickets(self)

	def on_cancel(self):
		issue = frappe.get_doc("Repair Issue", self.issue)
		issue.remove_tickets(self)

	def remove_all_reports(self):
		self.set("reports", list())

	def append_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted ticket"))

		current_reports = [d.report for d in self.get("reports")]
		for report in reports:
			if report.name in current_reports:
				continue
			self.append("reports", {"report": report.name})

		self.save()

	def remove_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted ticket"))

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
			throw(_("Current ticket is not in new state"))

		if self.assigned_to_user and self.asigned_to_user != frappe.session.user:
			throw(_("This ticket is assigned to {1}").format(self.assigned_to_user))
		else:
			self.assigned_to_user = frappe.session.user

		self.set('status', 'Fixing')
		self.save()

		frappe.msgprint(_("Your Got This Ticket"))

	def ticket_fixed(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixing':
			throw(_("Current ticket is not in fixing state"))

		if self.assigned_to_user != frappe.session.user:
			throw(_("This ticket is assigned to {1}").format(self.assigned_to_user))
		self.set('status', 'Fixed')
		self.save()

		frappe.msgprint(_("Ticket Fixed"))

	def ticket_close(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixed':
			throw(_("Current ticket is not in fixed state"))

		self.set('status', 'Closed')
		self.save()

		frappe.msgprint(_("Ticket Closed"))

	def ticket_reject(self):
		if self.docstatus == 2:
			return
		if self.status != 'Fixed':
			throw(_("Current ticket is not in fixed state"))

		self.set('status', 'Rejected')
		self.save()

		frappe.msgprint(_("Ticket Fix Rejected"))

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
				"value": _("Issue: {0}\nPrice: {1}\nInfo: {2}").format(self.issue, self.cost, self.issue_info)
			}
		}

	def wechat_tmsg_url(self):
		return "/update-repair-issue?name=" + self.name


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	sites = list_sites(user)

	# [frappe.db.escape(r) for r in frappe.get_roles(user)]

	return """(`tabRepair Ticket`.site in ({sites}))""".format(
		sites='"' + '", "'.join(sites) + '"')



def wechat_notify_by_ticket_name(issue_name, issue_doc=None):
	issue_doc = issue_doc or frappe.get_doc("Repair Issue", issue_name)

	user_list = {}
	# Get all teams for that site
	for st in frappe.db.get_values("Repair SiteTeam", {"parent": issue_doc.site}, "team"):
		ent = frappe.db.get_value("Repair Team", st[0], "enterprise")
		app = frappe.db.get_value("Repair Enterprise", ent, "wechat_app")
		if not app:
			app = frappe.db.get_single_value("Repair Settings", "default_wechat_app")
		if app:
			if not user_list.has_key(app):
				user_list[app] = []
			for d in frappe.db.get_values("Repair TeamUser", {"parent": st[0]}, "user"):
				user_list[app].append(d[0])
			"""
			frappe.sendmail(recipients=email_account.get_unreplied_notification_emails(),
				content=comm.content, subject=comm.subject, doctype= comm.reference_doctype,
				name=comm.reference_name)
			"""
	for app in user_list:
		#print("Send wechat notify : {0} to users {1} via app {2}".format(issue_doc.as_json(), user_list[app], app))
		from wechat.api import send_doc
		send_doc(app, 'Repair Issue', issue_doc.name, user_list[app])