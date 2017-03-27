from __future__ import unicode_literals
import frappe


def on_admin_insert(doc, method, user):
	frappe.get_doc('User', user).add_roles('Tickets Admin')


def on_admin_remove(doc, method, user):
	frappe.get_doc('User', user).remove_roles('Tickets Admin')

