frappe.listview_settings['Repair Issue'] = {
	onload: function(me) {
		frappe.route_options = {
			"owner": user,
			"status": "Open"
		};
	},
	refresh: function(me) {
		// add created by me
		me.page.add_sidebar_item(__("Created By Me"), function() {
			var assign_filter = me.filter_list.get_filter("owner");
			assign_filter && assign_filter.remove(true);

			me.filter_list.add_filter(me.doctype, "owner", '=', user);
			me.run();
		}, ".assigned-to-me");
	},
	add_fields: ["issue_source_type", "issue_source"],
}
