// Copyright (c) 2016, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Repair Issue', {
	setup: function(frm) {
		/*frm.fields_dict["fixed_by"].get_query = function(){
			return {
				filters: {"ignore_user_type": 1}
			};
		};*/
		/* frm.fields_dict["issue_source_type"].get_query = function(){
			return {
				filters: {
					"name": ["in","IOT Device Error,Repair Issue,IOT Device"]
				}
			}
		}; */
	},
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Create Ticket"), function() {
				 frappe.model.with_doctype('Repair Ticket', function() {
					var mr = frappe.model.get_new_doc('Repair Ticket');
					doc.issue = frm.doc.name
					//frappe.set_route('Form', 'Repair Ticket', mr.name);
				});
			});
			frm.custom_buttons[__("Create Ticket")].removeClass("btn-default");
			frm.custom_buttons[__("Create Ticket")].addClass("btn-primary");
		}
	}
});
