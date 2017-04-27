# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe import throw, _
from frappe.utils.data import format_datetime


class TicketsTask(Document):
	def validate(self):
		self.project = frappe.get_value(self.site_type, self.site, "project")
		if self.site_type == 'Cell Station':
			self.site_name = frappe.get_value(self.site_type, self.site, "station_name")
		if self.site_type == 'Cloud Project Site':
			self.site_name = frappe.get_value(self.site_type, self.site, "site_name")

	def wechat_tmsg_data(self):
		remark = _("Site: {0}").format(self.site) + "\n" + \
				_("Prioirty: {0}").format(self.total_cost) + "\n" + \
				_("Info: {0}").format(self.task_desc)
		return {
			"first": {
				"value": _("New Task Created"),
				"color": "red"
			},
			"keyword1": {
				"value": self.name,  # 编号
				"color": "blue"
			},
			"keyword2": {
				"value": self.task_name,  # 标题
				"color": "blue"
			},
			"keyword3": {
				"value": format_datetime(self.modified),  # 时间
				"color": "green",
			},
			"remark": {
				"value": remark
			}
		}

	def wechat_tmsg_url(self):
		return "/update-tickets-task?name=" + self.name

	def update_cost(self):
		tickets = self.get("tickets")
		self.total_cost = 0
		for ticket in tickets:
			self.total_cost += frappe.get_value("Tickets Ticket", ticket.ticket, "cost")
		self.save()

	def append_tickets(self, *tickets):
		if self.docstatus != 1:
			throw(_("Cannot append tickets on un-submitted task"))

		current_tickets = [d.ticket for d in self.get("tickets")]
		for ticket in tickets:
			if ticket.name in current_tickets:
				continue
			self.append("tickets", {"ticket": ticket.name})

		self.update_cost()

	def remove_tickets(self, *tickets):
		if self.docstatus != 1:
			throw(_("Cannot append tickets on un-submitted task"))

		existing_tickets = dict((d.ticket, d) for d in self.get("tickets"))
		for ticket in tickets:
			if ticket.name in existing_tickets:
				self.get("tickets").remove(existing_tickets[ticket.name])

		self.update_cost()


def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("Tickets Tasks"),
		"row_template": "templates/generators/tickets_task_row.html",
	}


def get_permission_query_conditions(user):
	if 'Tickets Manager' in frappe.get_roles(user):
		return ""

	from cloud.cloud.doctype.cloud_project.cloud_project import list_admin_projects
	projects = list_admin_projects(user)

	if len(projects) != 0:
		return """(`tabTickets Task`.owner = "{user}" or `tabTickets Task`.project in ({projects}))""".format(
			user = user,
			projects='"' + '", "'.join(projects) + '"')

	return """(`tabTickets Task`.owner = '{0}')""".format(user)
