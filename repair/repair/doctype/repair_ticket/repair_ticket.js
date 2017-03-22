// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Repair Ticket', {
	refresh: function(frm) {
		frm.clear_custom_buttons();
		if(frm.doc.docstatus == 1 && frm.doc.status=='New') {
			frm.add_custom_button(__("Get It"), function() {
				frm.events.ticket_event(frm, "ticket_get");
			});
			frm.custom_buttons[__("Get It")].removeClass("btn-default");
			frm.custom_buttons[__("Get It")].addClass("btn-primary");
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=='Fixing' && frm.doc.assigned_to_user==user) {
			frm.add_custom_button(__("Create Report"), function() {
				 frappe.model.with_doctype('Repair Report', function() {
					var mr = frappe.model.get_new_doc('Repair Report');
					mr.ticket = frm.doc.name;
					mr.title = __("Report for ") + frm.doc.name;
					mr.site = frm.doc.site;
					frappe.set_route('Form', mr.doctype, mr.name);
				});
			});
			frm.custom_buttons[__("Create Report")].removeClass("btn-default");
			frm.custom_buttons[__("Create Report")].addClass("btn-primary");

			frm.add_custom_button(__("Fixed"), function() {
				frm.events.ticket_event(frm, "ticket_fixed");
			});
			frm.custom_buttons[__("Fixed")].removeClass("btn-default");
			frm.custom_buttons[__("Fixed")].addClass("btn-success");
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=='Fixed') {
			if(has_common(roles, ["Administrator", "System Manager", "IOT Manager"]) && !frm.doc.__islocal) {
				frm.add_custom_button(__("Close"), function() {
					frm.events.ticket_event(frm, "ticket_close");
				});
				frm.custom_buttons[__("Close")].removeClass("btn-default");
				frm.custom_buttons[__("Close")].addClass("btn-success");

				frm.add_custom_button(__("Reject"), function() {
					frm.events.ticket_event(frm, "ticket_reject");
				});
				frm.custom_buttons[__("Reject")].removeClass("btn-default");
				frm.custom_buttons[__("Reject")].addClass("btn-warning");
			}
		}
	},

	ticket_event: function(frm, event) {
		return frappe.call({
			doc: frm.doc,
			method: event,
			freeze: true,
			callback: function(r) {
				if(!r.exc)
					frm.refresh_fields();
					frm.events.refresh(frm);
			}
		})
	},
});
