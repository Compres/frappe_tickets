// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Ticket Bundle', {
	setup: function (frm) {
		frm.fields_dict['tickets'].grid.get_field("ticket").get_query =
			"tickets.tickets.doctype.tickets_ticket_bundle.tickets_ticket_bundle.ticket_query"
	},
	refresh: function(frm) {
		frm.clear_custom_buttons();
		if(frm.doc.docstatus == 1 && !frm.doc.assigned_to_user) {
			frm.add_custom_button(__("Get It"), function() {
				frm.events.bundle_event(frm, "bundle_get");
			});
			frm.custom_buttons[__("Get It")].removeClass("btn-default");
			frm.custom_buttons[__("Get It")].addClass("btn-primary");
		}
		if(frm.doc.docstatus == 1 && frm.doc.assigned_to_user==user) {
			frm.add_custom_button(__("Fixed"), function() {
				frm.events.bundle_event(frm, "bundle_fixed");
			});
			frm.custom_buttons[__("Fixed")].removeClass("btn-default");
			frm.custom_buttons[__("Fixed")].addClass("btn-success");
		}
	},
	bundle_event: function(frm, event) {
		return frappe.call({
			doc: frm.doc,
			method: event,
			freeze: true,
			callback: function(r) {
				if(!r.exc)
					frm.refresh_fields();
					frm.events.refresh(frm);
			}
		});
	}
});
