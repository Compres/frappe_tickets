# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from repair.repair.doctype.repair_site.repair_site import list_sites

class RepairReport(Document):
	def on_submit(self):
		ticket = frappe.get_doc("Repair Ticket", self.ticket)
		ticket.append_reports(self)

	def on_cancel(self):
		ticket = frappe.get_doc("Repair Ticket", self.ticket)
		ticket.remove_reports(self)


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	sites = list_sites(user)

	# [frappe.db.escape(r) for r in frappe.get_roles(user)]

	return """(`tabRepair Ticket`.site in ({sites}))""".format(
		sites='"' + '", "'.join(sites) + '"')
