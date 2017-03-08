frappe.listview_settings['Repair Issue'] = {
	get_indicator: function(doc) {
		if(doc.status == "New") {
			return [__("New"), "red", "status,=,New"];
		}
		else if(doc.status == "Open") {
			return [__("Open"), "orange", "status,=,Open"];
		}
		else if(doc.status == "Fixed") {
			return [__("Fixed"), "green", "status,=,Fixed"];
		}
		else if(doc.status == "Closed") {
			return [__("Closed"), "darkgrey", "status,=,Closed"];
		}
	},
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
