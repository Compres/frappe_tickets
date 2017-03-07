// Copyright (c) 2016, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Repair Issue', {
	setup: function(frm) {
		frm.fields_dict["fixed_by"].get_query = function(){
			return {
				filters: {"ignore_user_type": 1}
			};
		};
		frm.fields_dict["issue_source_type"].get_query = function(){
			return {
				filters: {
					"name": ["in","IOT Device Error,Repair Issue,IOT Device"]
				}
			}
		};
	},
	refresh: function(frm) {

	}
});
