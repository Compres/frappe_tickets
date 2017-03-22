# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RepairTicket(Document):
	def on_submit(self):
		issue = frappe.get_doc("Repair Issue", self.issue)
		issue.submit_ticket_cost(self.cost)
