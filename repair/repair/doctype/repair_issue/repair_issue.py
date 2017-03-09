# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe import _


class RepairIssue(Document):

	def validate(self):
		if self.status == 'Closed':
			self.fixed_by = frappe.session.user
			self.fixed_date = frappe.utils.data.now()
		else:
			self.fixed_by = None
			self.fixed_date = None

	def on_update(self):
		if self.wechat_notify == 1 and self.wechat_sent != 1:
			frappe.enqueue('repair.repair.doctype.repair_issue.repair_issue.wechat_notify_by_issue_name',
							issue_name = self.name)

	def has_website_permission(self, ptype, verbose=False):
		user = frappe.session.user
		if self.fixed_by == user:
			return True

		teams = [d[0] for d in frappe.db.get_values('Repair SiteTeam', {"parent": self.site}, "team")]

		for team in teams:
			if frappe.get_value('Repair TeamUser', {"parent": team, "user": user}):
				return True

		return False


def get_issue_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified desc"):
	return frappe.db.sql('''select distinct issue.*
		from `tabRepair Issue` issue, `tabRepair TeamUser` team_user, `tabRepair SiteTeam` site_team
		where (issue.site = site_team.parent
			and site_team.team = team_user.parent 
			and team_user.user = %(user)s)
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


def list_user_sites(user=None):
	if not user:
		user = frappe.session.user

	teams = [d[0] for d in frappe.db.get_values('Repair TeamUser', {"user": user}, "parent")]
	sites = []
	for team in teams:
		for d in frappe.db.get_values('Repair SiteTeam', {'team': team}, "parent"):
			sites.append(d[0])

	return sites


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	else:
		return """(`tabRepair Issue`.site in ({user_sites}))""".format(
			user_sites='"' + '", "'.join(list_user_sites(user)) + '"')


def has_permission(doc, user):
	if 'Repair Manager' in frappe.get_roles(user):
		return True

	if doc.fixed_by == user:
		return True

	teams = [d[0] for d in frappe.db.get_values('Repair SiteTeam', {"parent": doc.site}, "team")]

	for team in teams:
		if frappe.get_value('Repair TeamUser', {"parent": team, "user": user}):
			return True

	return False


def wechat_notify_by_issue_name(issue_name):
	issue_doc = frappe.get_doc("Repair Issue", issue_name)
	if issue_doc.wechat_sent == 1:
		return

	if issue_doc.status in ["New", "Open"]:
		# Get all teams for that site
		for st in frappe.db.get_values("Repair SiteTeam", {"parent": issue_doc.site}, "team"):
			users = [d[0] for d in frappe.db.get_values("Repair TeamUser", {"parent": st[0]}, "user")]
			print("Send wechat notify : {0} to users {1} ".format(issue_doc.as_json(), users))
			"""
			frappe.sendmail(recipients=email_account.get_unreplied_notification_emails(),
				content=comm.content, subject=comm.subject, doctype= comm.reference_doctype,
				name=comm.reference_name)
			"""

	# update flag
	issue_doc.db_set("wechat_sent", 1)


def wechat_notify():
	"""Sends WeChat notifications if there are un-notified issues
		and `wechat_sent` is set as true."""

	for issue in frappe.get_all("Repair Issue", "name", filters={"wechat_notify": 1, "wechat_sent": 0}):
		wechat_notify_by_issue_name(issue.name)


@frappe.whitelist()
def list_site_map():
	issues = frappe.get_all('Repair Issue',
							 fields=["name", "issue_name", "site", "priority", "price", "status"])
	for issue in issues:
		issue.longitude = frappe.get_value('Repair Site', issue.site, "longitude") or 116.3252
		issue.latitude = frappe.get_value('Repair Site', issue.site, "latitude") or '40.045103'
	return issues
