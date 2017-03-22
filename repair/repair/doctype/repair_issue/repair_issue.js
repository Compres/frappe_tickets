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
		if(frm.doc.docstatus == 1 && has_common(roles, ["Administrator", "Repair Admin"])){
			frm.add_custom_button(__("Create Ticket"), function() {
				 frappe.model.with_doctype('Repair Ticket', function() {
					var mr = frappe.model.get_new_doc('Repair Ticket');
					mr.issue = frm.doc.name;
					mr.issue_info = frm.doc.issue_desc;
					mr.site = frm.doc.site;
					frappe.set_route('Form', mr.doctype, mr.name);
				});
			});
			frm.custom_buttons[__("Create Ticket")].removeClass("btn-default");
			frm.custom_buttons[__("Create Ticket")].addClass("btn-primary");

			frm.add_custom_button(__("Update Cost"), function() {
				frm.events.update_cost(frm);
			});
			frm.custom_buttons[__("Update Cost")].removeClass("btn-default");
			frm.custom_buttons[__("Update Cost")].addClass("btn-warning");
		}
	},

	update_cost: function(frm) {
		return frappe.call({
			doc: frm.doc,
			method: "update_cost",
			freeze: true,
			callback: function(r) {
				if(!r.exc) frm.refresh_fields();
			}
		})
	},
});
