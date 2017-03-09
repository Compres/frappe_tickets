# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RepairTeamUser(Document):
	def validate(self):
		if 'Repair Enterprise Admin' in frappe.get_roles(self.user):
			frappe.throw(frappe._("User {0} is an Enterprise Admin").format(self.user))

	def after_insert(self):
		# Make sure it has Repair User permission
		if 'Repair User' not in frappe.get_roles(self.user):
			user = frappe.get_doc('User', self.user)
			user.add_roles('Repair User')