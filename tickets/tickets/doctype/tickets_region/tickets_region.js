// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Region', {
	setup: function(frm) {
		frm.fields_dict['team_assigned'].grid.get_field("team").get_query = function(){
			return {
				query:"tickets.tickets.doctype.tickets_region.tickets_region.query_team"
				searchfield:"group_name"
			}
		}
		frm.fields_dict['region'].get_query = function(){
			return {
				query:"tickets.tickets.doctype.tickets_region.tickets_region.query_region",
				searchfield:"region_name"
			}
		}
	},
	refresh: function(frm) {

	}
});