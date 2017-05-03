// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tickets Ticket', {
	setup: function(frm) {

	},
	refresh: function(frm) {
		frm.clear_custom_buttons();
		if(frm.doc.docstatus == 1 && frm.doc.status=='New') {
			frm.add_custom_button(__("Get It"), function() {
				frm.events.ticket_event(frm, "ticket_get");
			}).removeClass("btn-default").addClass("btn-primary");
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=='Fixing' && frm.doc.assigned_to_user==user) {
			frm.add_custom_button(__("Create Report"), function() {
				 frappe.model.with_doctype('Tickets Report', function() {
					var mr = frappe.model.get_new_doc('Tickets Report');
					mr.project = frm.doc.project;
					mr.ticket = frm.doc.name;
					mr.title = __("Report for ") + frm.doc.name;
					mr.site = frm.doc.site;
					frappe.set_route('Form', mr.doctype, mr.name);
				});
			}).removeClass("btn-default").addClass("btn-primary");

			frm.add_custom_button(__("Fixed"), function() {
				frm.events.ticket_event(frm, "ticket_fixed");
			}).removeClass("btn-default").addClass("btn-success");

			if (frm.custom_buttons[__('Create Delivery Order')]) {
				frm.custom_buttons[__('Create Delivery Order')].removeClass("hidden");
			} else {
				frm.events.onload_post_render(frm);
			}
		}
		if(frm.doc.docstatus == 1 && frm.doc.status=='Fixed') {
			if (has_common(roles, ["Administrator", "System Manager", "IOT Manager"]) && !frm.doc.__islocal) {
				frm.add_custom_button(__("Close"), function () {
					frm.events.ticket_event(frm, "ticket_close");
				}).removeClass("btn-default").addClass("btn-success");

				frm.add_custom_button(__("Reject"), function () {
					frm.events.ticket_event(frm, "ticket_reject");
				}).removeClass("btn-default").addClass("btn-warning");
			}
		}
	},
	onload_post_render: function(frm) {
		frappe.call({
			type: "GET",
			method: "tickets.tickets.doctype.tickets_ticket.tickets_ticket.is_stock_installed",
			callback: function (r, rt) {
				if (r.message) {
					frm.toggle_display("item_list", true);
					frm.toggle_display("items", true);
					frm.events.show_gen_entry(frm);
				}
			}
		});
	},
	show_gen_entry: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.status=='Fixing' && frm.doc.assigned_to_user==user) {
			frm.add_custom_button(__('Create Delivery Order'), function () {
				return frappe.call({
					doc: frm.doc,
					method: "create_delivery_order",
					freeze: true,
					callback: function (r) {
						if (!r.exc) {
							frm.refresh_fields();
							frm.custom_buttons[__('Create Delivery Order')].addClass('hidden');
						}
					}
				});
			}).removeClass("btn-default").addClass("btn-primary");

			if (frm.doc.delivery_order) {
				frm.custom_buttons[__('Create Delivery Order')].addClass("hidden");
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
		});
	}
});

frappe.ui.form.on('Tickets TicketItem', {
	item: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Stock Item",
				name: d.item,
				filters: {
					docstatus: 1
				}
			},
			callback: function(r, rt) {
				if(r.message) {
					frappe.model.set_value(cdt, cdn, "item_name", r.message.item_name);
					frappe.model.set_value(cdt, cdn, "uom", r.message.stock_uom);
				}
			}
		});
	}
});
