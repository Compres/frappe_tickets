frappe.listview_settings['Repair Issue'] = {
	/*get_indicator: function(doc) {
		colour = {'New': 'red', 'Open': 'orange', 'Fixed': 'blue', 'Closed': 'darkgrey'};
		return [__(doc.status), colour[doc.status], "status,=," + doc.status];
	},*/
	onload: function(me) {
		frappe.route_options = {
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
