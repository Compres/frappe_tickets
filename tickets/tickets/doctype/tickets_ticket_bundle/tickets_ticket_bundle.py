# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import getdate, nowdate
from frappe.model.document import Document

class TicketsTicketBundle(Document):
	def validate(self):
		cost = 0
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket.ticket)
			if doc.assigned_to_user is not None:
				throw(_("Ticket {0} is already assigned to user {1}").format(ticket.ticket, doc.assigned_to_user))
			if getdate(doc.planned_end_date) > getdate(self.planned_end_date):
				throw(_("Ticket {0} planned date is late than bundle's {1}").format(doc.planned_end_date, self.planned_end_date))
			cost += doc.cost

		self.total_cost = cost

	def on_submit(self):
		if self.assigned_to_user:
			for ticket in self.tickets:
				doc = frappe.get_doc("Tickets Ticket", ticket)
				doc.assigned_to_user = self.assigned_touser
				doc.save()

		if self.wechat_notify == 1:
			frappe.enqueue('tickets.tickets.doctype.tickets_ticket_bundle.tickets_ticket_bundle.wechat_notify', bundle=self)

	def bundle_get(self):
		self.assigned_to_user = frappe.session.user
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket.ticket)
			doc.assigned_to_user = self.assigned_touser
			doc.save()

		self.save()

	def bundle_fixed(self):
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket.ticket)
			assert(doc.status == "Fixed")

		self.actual_end_date = getdate(nowdate())
		self.save()

	def update_cost(self):
		cost = 0
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket.ticket)
			cost += doc.cost

		self.total_cost = cost
		self.save()

	def wechat_tmsg_data(self):
		return {
			"first": {
				"value": _("New Ticket Bundle Created"),
				"color": "red"
			},
			"keyword1": {
				"value": self.name,  # 编号
				"color": "blue"
			},
			"keyword2": {
				"value": self.bundle_name,  # 标题
				"color": "blue"
			},
			"keyword3": {
				"value": self.planned_end_date,  # 时间
				"color": "green",
			},
			"remark": {
				"value": _("Total Cost: {0}").format(self.total_cost)
			}
		}

	def wechat_tmsg_url(self):
		return "/desk#Form/Tickets Ticket Bundle/" + self.name


def ticket_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name, ticket_name from `tabTickets Ticket`
		where docstatus = 1 and assigned_to_user is null and status = 'New'
		and %s like %s order by name limit %s, %s""" %
		(searchfield, "%s", "%s", "%s"),
		("%%%s%%" % txt, start, page_len), as_list=1)


def wechat_notify(bundle=None):
	from cloud.cloud.doctype.cloud_company.cloud_company import get_wechat_app
	from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_users
	from wechat.api import send_doc

	teams = None
	for ticket in bundle.tickets:
		ticket_doc = frappe.get_doc("Tickets Ticket", ticket.ticket)

		# Get all teams for that site
		tlist = [st[0] for st in frappe.db.get_values("Tickets SiteTeam",
						{"parent": ticket_doc.site, "type": ticket_doc.task_type}, "team")]
		org_tlist = teams or tlist
		teams = [val for val in tlist if val in org_tlist]

	user_list = {}
	for team in teams:
		app = get_wechat_app(frappe.db.get_value("Cloud Company Group", team, "company"))
		if app:
			if not user_list.has_key(app):
				user_list[app] = []
			for d in list_users(st[0]):
				user_list[app].append(d.name)

	for app in user_list:
		send_doc(app, 'Tickets Ticket Bundle', bundle.name, user_list[app])
