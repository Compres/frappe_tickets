# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RepairReport(Document):
	def on_submit(self):
		ticket = frappe.get_doc("Repair Ticket", self.ticket)
		ticket.append_reports(self)

	def on_cancel(self):
		ticket = frappe.get_doc("Repair Ticket", self.ticket)
		ticket.remove_reports(self)
