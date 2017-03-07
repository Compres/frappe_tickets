# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class RepairSite(Document):

	def autoname(self):
		"""set name as [self.parent].<name>"""
		self.site_name = self.site_name.strip()
		self.name = '[' + self.enterprise + '].' + self.site_name

	def has_website_permission(self, ptype, verbose=False):
		print('has_website_permission', self.name)
		return True
