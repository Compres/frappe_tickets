# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from tickets.tickets.doctype.tickets_site.tickets_site import list_admin_sites

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

	sites = list_admin_sites(user)
	if len(sites) != 0:
		return """(`tabTickets Report`.owner = '{user}' or `tabTickets Report`.site in ({sites}))""".format(
			user = user,
			sites='"' + '", "'.join(sites) + '"')

	return """(`tabTickets Report`.owner = '{0}')""".format(user)
