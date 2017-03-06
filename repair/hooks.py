# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "repair"
app_title = "Repair"
app_publisher = "Dirk Chang"
app_description = "Repair Suppliers"
app_icon = "octicon octicon-file-directory"
app_color = "orange"
app_email = "dirk.chang@symid.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/repair/css/repair.css"
# app_include_js = "/assets/repair/js/repair.js"

# include js, css files in header of web template
# web_include_css = "/assets/repair/css/repair.css"
# web_include_js = "/assets/repair/js/repair.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "repair.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Website Route Rules
website_route_rules = [
	{"from_route": "/repair_issues", "to_route": "Repair Issue"},
	{"from_route": "/repair_issues/<path:name>", "to_route": "update-repair-issue",
		"defaults": {
			"doctype": "Repair Issue",
			"parents": [{"title": _("Repair Issues"), "name": "repair_issues"}]
		}
	},
]

portal_menu_items = [
	{"title": _("Repair Issues"), "route": "/repair_issues", "reference_doctype": "Repair Issue", "role": "Repair User"}
]

# Installation
# ------------

# before_install = "repair.install.before_install"
# after_install = "repair.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "repair.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"repair.tasks.all"
# 	],
# 	"daily": [
# 		"repair.tasks.daily"
# 	],
# 	"hourly": [
# 		"repair.tasks.hourly"
# 	],
# 	"weekly": [
# 		"repair.tasks.weekly"
# 	]
# 	"monthly": [
# 		"repair.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "repair.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "repair.event.get_events"
# }

