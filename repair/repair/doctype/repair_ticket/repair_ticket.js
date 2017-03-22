// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Repair Ticket', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__("Get It"), function() {
				 frappe.model.with_doctype('Repair Ticket Result', function() {
					var mr = frappe.model.get_new_doc('Repair Ticket Result');
					mr.ticket = frm.doc.name;
					frappe.set_route('Form', mr.doctype, mr.name);
				});
			});
			frm.custom_buttons[__("Get It")].removeClass("btn-default");
			frm.custom_buttons[__("Get It")].addClass("btn-primary");
		}
	}
});
