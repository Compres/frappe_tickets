// Copyright (c) 2016, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Site', {
	setup: function(frm) {
		frm.fields_dict['team_assigned'].grid.get_field("team").get_query = function(){
			return {
				query:"tickets.tickets.doctype.tickets_site.tickets_site.query_team"
			}
		}
	},
	refresh: function(frm) {

	}
});
