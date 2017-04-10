# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, nowdate
from frappe.model.document import Document

class TicketsTicketBundle(Document):
	def validate(self):
		cost = 0
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket)
			assert(doc.assigned_to_user is None)
			assert(doc.doc_status == 1)
			assert(doc.status == 'New')
			assert(doc.planned_end_date <= self.planned_end_date)
			cost += doc.cost

		self.total_cost = cost

	def on_submit(self):
		if self.assigned_to_user:
			for ticket in self.tickets:
				doc = frappe.get_doc("Tickets Ticket", ticket)
				doc.assigned_to_user = self.assigned_touser
				doc.save()

	def bundle_get(self):
		self.assigned_to_user = frappe.session.user
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket)
			doc.assigned_to_user = self.assigned_touser
			doc.save()

		self.save()

	def bundle_fixed(self):
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket)
			assert(doc.status == "Fixed")

		self.actual_end_date = getdate(nowdate())
		self.save()

	def update_cost(self):
		cost = 0
		for ticket in self.tickets:
			doc = frappe.get_doc("Tickets Ticket", ticket)
			cost += doc.cost

		self.total_cost = cost
		self.save()