# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies


class RepairSite(Document):

	def has_website_permission(self, ptype, verbose=False):
		print('has_website_permission', self.name)
		return True


def list_user_sites(user=None):
	if not user:
		user = frappe.session.user

	teams = [d[0] for d in frappe.db.get_values('Repair TeamUser', {"user": user}, "parent")]
	sites = []
	for team in teams:
		for d in frappe.db.get_values('Repair SiteTeam', {'team': team}, "parent"):
			sites.append(d[0])

	return sites


def list_company_sites(company):
	return [d[0] for d in frappe.db.get_values('Repair Site', {"company": company}, "name")]


def get_permission_query_conditions(user):
	if 'Repair Manager' in frappe.get_roles(user):
		return ""

	return """(`tabRepair Site`.company in ({clist}))""".format(
		clist='"' + '", "'.join(list_admin_companies(user)) + '"')


def has_permission(doc, user):
	if 'Repair Manager' in frappe.get_roles(user):
		return True

	companies = list_admin_companies(user)
	return doc.company in companies


@frappe.whitelist()
def list_site_map():
	sites = list_user_sites(frappe.session.user)

	sites = frappe.get_all('Repair Site', filters={"name": ["in", sites]},
							fields=["name", "site_name", "longitude", "latitude", "address", "enterprise"])
	for dev in sites:
		if not dev.longitude:
			dev.longitude = '116.3252'
		if not dev.latitude:
			dev.latitude = '40.045103'
	return sites
