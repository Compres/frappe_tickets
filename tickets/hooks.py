# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "tickets"
app_title = "Tickets"
app_publisher = "Dirk Chang"
app_description = "Tickets Suppliers"
app_icon = "octicon octicon-file-directory"
app_color = "orange"
app_email = "dirk.chang@symid.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tickets/css/tickets.css"
# app_include_js = "/assets/tickets/js/tickets.js"

# include js, css files in header of web template
# web_include_css = "/assets/tickets/css/tickets.css"
# web_include_js = "/assets/tickets/js/tickets.js"

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
# get_website_user_home_page = "tickets.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Website Route Rules
website_route_rules = [
	{"from_route": "/tickets_tasks", "to_route": "Tickets Task"},
	{"from_route": "/tickets_tasks/<path:name>", "to_route": "update-tickets-task",
		"defaults": {
			"doctype": "Tickets Task",
			"parents": [{"title": _("Tickets Tasks"), "name": "tickets_tasks"}]
		}
	},
]

# portal_menu_items = [
# 	{"title": _("Tickets Tasks"), "route": "/tickets_tasks", "reference_doctype": "Tickets Task", "role": "Tickets User"},
# 	{"title": _("Tickets Ticket Map"), "route": "/tickets_ticket_map", "role": "Tickets User"}
# ]

# Installation
# ------------

# before_install = "tickets.install.before_install"
# after_install = "tickets.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tickets.notifications.get_notification_config"

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

permission_query_conditions = {
	"Tickets Task": "tickets.tickets.doctype.tickets_task.tickets_task.get_permission_query_conditions",
	"Tickets Region": "tickets.tickets.doctype.tickets_region.tickets_region.get_permission_query_conditions",
	"Tickets Ticket": "tickets.tickets.doctype.tickets_ticket.tickets_ticket.get_permission_query_conditions",
	"Tickets Report": "tickets.tickets.doctype.tickets_report.tickets_report.get_permission_query_conditions",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "User": {
	# 	"after_insert": "tickets.controllers.user_hooks.after_insert",
	# },
	"Cloud Company": {
		"on_admin_insert": "tickets.controllers.company_hooks.on_admin_insert",
		"on_admin_remove": "tickets.controllers.company_hooks.on_admin_remove",
	}
}

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
# 		"tickets.tasks.all"
# 	],
# 	"daily": [
# 		"tickets.tasks.daily"
# 	],
# 	"hourly": [
# 		"tickets.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tickets.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tickets.tasks.monthly"
# 	]
# }


# Testing
# -------

# before_tests = "tickets.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tickets.event.get_events"
# }

