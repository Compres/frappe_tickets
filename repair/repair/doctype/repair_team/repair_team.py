# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class RepairTeam(Document):

	def autoname(self):
		"""set name as [self.parent].<name>"""
		self.team_name = self.team_name.strip()
		self.name = '[' + self.enterprise + '].' + self.team_name
