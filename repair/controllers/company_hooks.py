from __future__ import unicode_literals


def on_admin_insert(doc, method, user):
	doc.add_roles('Repair Admin')


def on_admin_remove(doc, method, user):
	doc.remove_roles('Repair Admin')

