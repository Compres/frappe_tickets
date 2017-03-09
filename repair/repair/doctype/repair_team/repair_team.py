# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from repair.repair.doctype.repair_enterprise.repair_enterprise import list_user_enterpries


class RepairTeam(Document):

	def autoname(self):
		"""set name as [self.parent].<name>"""
		self.team_name = self.team_name.strip()
		self.name = '[' + self.enterprise + '].' + self.team_name


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	return """(`tabRepair Team`.enterprise in ({user_ents}))""".format(
		user_ents='"' + '", "'.join(list_user_enterpries(user)) + '"')


def has_permission(doc, user):
	if 'Repair Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Repair Enterprise', {'admin': user, 'name': doc.enterprise}):
		return True

	return False
