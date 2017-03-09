# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RepairEnterprise(Document):

	def on_update(self):
		org_admin = frappe.db.get_value("Repair Enterprise", {"name": self.name}, "admin")
		if org_admin != self.admin:
			user = frappe.get_doc('User', org_admin)
			user.remove_roles('Repair Enterprise Admin')
			user.add_roles('Repair User')
		user = frappe.get_doc('User', self.admin)
		user.add_roles('Repair Enterprise Admin')
		user.remove_roles('Repair User')


def list_user_enterpries(user=None):
	if not user:
		user = frappe.session.user

	return [d[0] for d in frappe.db.get_values('Repair Enterprise', {'admin': user}, 'name')]


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	return '''(`tabRepair Enterprise`.admin = "{0}")'''.format(user)


def has_permission(doc, user):
	if 'Repair Manager' in frappe.get_roles(user):
		return True

	return doc.admin == user
