# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document

class RepairTicket(Document):
	def on_submit(self):
		issue = frappe.get_doc("Repair Issue", self.issue)
		issue.submit_ticket_cost(self.cost)

	def remove_all_reports(self):
		self.set("reports", list())

	def append_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted ticket"))
		"""Add reports to user"""
		current_reports = [d.ticket for d in self.get("reports")]
		for report in reports:
			if report.name in current_reports:
				continue
			self.append("reports", report)

		self.save()

	def remove_reports(self, *reports):
		if self.docstatus != 1:
			throw(_("Cannot append reports on un-submitted ticket"))

		existing_reports = dict((d.ticket, d) for d in self.get("reports"))
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