// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Task', {
	setup: function(frm) {
		/*frm.fields_dict["fixed_by"].get_query = function(){
			return {
				filters: {"ignore_user_type": 1}
			};
		};*/
		frm.fields_dict["site_type"].get_query = function(){
			return {
				filters: {
					"name": ["in",["Cell Station","Cloud Project Site"]]
				}
			}
		};
	},
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && has_common(roles, ["Administrator", "Tickets Admin"])){
			frm.add_custom_button(__("Create Ticket"), function() {
				 frappe.model.with_doctype('Tickets Ticket', function() {
					var mr = frappe.model.get_new_doc('Tickets Ticket');
					mr.ticket_name = frm.doc.task_name + " Ticket";
					mr.task = frm.doc.name;
					mr.task_info = frm.doc.task_desc;
					mr.task_type = frm.doc.task_type;
					mr.site_type = frm.doc.site_type;
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
