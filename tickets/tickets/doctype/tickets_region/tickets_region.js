// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Region', {
	setup: function(frm) {
		frm.fields_dict['team_assigned'].grid.get_field("team").get_query = function(){
			return {
				filters: {"enabled": 1}
			}
		};
	},
	refresh: function(frm) {

	}
});