# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class TicketsReport(Document):
	def on_submit(self):
		ticket = frappe.get_doc("Tickets Ticket", self.ticket)
		ticket.append_reports(self)

	def on_cancel(self):
		ticket = frappe.get_doc("Tickets Ticket", self.ticket)
		ticket.remove_reports(self)


def get_permission_query_conditions(user):
	if 'Tickets Manager' in frappe.get_roles(user):
		return ""

	from cloud.cloud.doctype.cloud_project.cloud_project import list_user_projects
	projects = list_user_projects(frappe.session.user)
	if len(projects) != 0:
		return """(`tabTickets Report`.owner = '{user}' or `tabTickets Report`.project in ({projects}))""".format(
			user = user,
			projects='"' + '", "'.join(projects) + '"')

	return """(`tabTickets Report`.owner = '{0}')""".format(user)
