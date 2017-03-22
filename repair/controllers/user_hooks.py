from __future__ import unicode_literals


def after_insert(doc, method):
	doc.add_roles('Repair User')

