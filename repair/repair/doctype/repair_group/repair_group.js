// Copyright (c) 2016, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Repair Group', {
	setup: function(frm) {
		frm.fields_dict["user_list"].grid.get_field('repair_user').get_query = function(){
			return {
				filters: {"ignore_user_type": 1}
			};
		};

		frm.fields_dict["user_list"].get_query = function(){
			return {
				filters: {"ignore_user_type": 1}
			};
		};
	},
	refresh: function(frm) {

	}
});
