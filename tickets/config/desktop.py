# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Tickets",
			"color": "orange",
			"icon": "fa fa-gavel",
			"type": "module",
			"label": _("Tickets")
		}
	]
