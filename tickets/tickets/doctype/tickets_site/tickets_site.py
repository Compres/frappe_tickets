# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class TicketsSite(Document):
	def validate(self):
		self.site_name = frappe.get_value("Cloud Project Site", self.site, 'site_name')

	def has_website_permission(self, ptype, verbose=False):
		print('has_website_permission', self.name)
		return True


def list_admin_sites(user, check_enable=True):
	from cloud.cloud.doctype.cloud_project_site.cloud_project_site import list_admin_sites

	sites = list_admin_sites(user, check_enable=check_enable)
	if len(sites) == 0:
		return []
	filters = {"site": ["in", sites]}
	if check_enable:
		filters["enabled"] = 1
	return [d[0] for d in frappe.db.get_values("Tickets Site", filters=filters)]


def list_user_sites(user=None, type=None):
	from cloud.cloud.doctype.cloud_company_group.cloud_company_group import list_user_groups

	teams = list_user_groups(user)
	sites = []
	for team in teams:
		filters = {'team': team}
		if type:
			filters['type'] = type
		for d in frappe.db.get_values('Tickets SiteTeam', filters, "parent"):
			sites.append(d[0])

	for d in list_admin_sites(user):
		sites.append(d)

	return sites


def get_permission_query_conditions(user):
	if 'Tickets Manager' in frappe.get_roles(user):
		return ""

	return """(`tabTickets Site`.site in ({sites}))""".format(
		sites='"' + '", "'.join(list_admin_sites(user)) + '"')


def query_team(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select name, concat_ws(" | ", company, group_name) from `tabCloud Company Group`
		where enabled = 1
		and %s like %s order by name limit %s, %s""" %
		(searchfield, "%s", "%s", "%s"),
		("%%%s%%" % txt, start, page_len), as_list=1)


@frappe.whitelist()
def list_site_map():
	sites = list_user_sites(frappe.session.user)
	if len(sites) == 0:
		return []

	sites = frappe.get_all('Tickets Site', filters={"name": ["in", sites]},
							fields=["name", "site_name", "longitude", "latitude", "address", "company"])
	for dev in sites:
		if not dev.longitude:
			dev.longitude = '116.3252'
		if not dev.latitude:
			dev.latitude = '40.045103'
	return sites
