# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class RepairIssue(Document):

	def has_website_permission(self, ptype, verbose=False):
		user = frappe.session.user
		if self.fixed_by == user:
			return True

		groups = [d[0] for d in frappe.db.get_values('Repair SiteGroup', {"parent": self.name}, "group")]

		for g in groups:
			if frappe.get_value('Repair GroupUser', {"parent": g, "user": user}):
				return True

		return False


def get_issue_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified desc"):
	return frappe.db.sql('''select distinct issue.*
		from `tabRepair Issue` issue, `tabRepair GroupUser` group_user, `tabRepair SiteGroup` site_group, 
		where issue.site = site_group.parent
			and site_group.group = group_user.parent 
			and group_user.user = %(user)s
			order by issue.{0}
			limit {1}, {2}
		'''.format(order_by, limit_start, limit_page_length),
			{'user':frappe.session.user},
			as_dict=True,
			update={'doctype':'Repair Issue'})


def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("Repair Issues"),
		"get_list": get_issue_list,
		"row_template": "templates/generators/repair_issue_row.html",
	}
