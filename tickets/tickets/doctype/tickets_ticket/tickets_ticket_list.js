/**
 * Created by cch on 17-4-6.
 */
frappe.listview_settings['Tickets Ticket'] = {
	get_indicator: function(doc) {
		colour = {'New': 'red', 'Fixing': 'orange', 'Fixed': 'blue', 'Closed': 'green', 'Rejected': 'darkgrey'};
		return [__(doc.status), colour[doc.status], "status,=," + doc.status];
	},
	onload: function(me) {
		frappe.route_options = {
			"status": ['in', "New,Fixing,Fixed"]
		};
	},
	refresh: function(me) {
		// add created by me
		me.page.add_sidebar_item(__("Not Closed Tickets"), function() {
			var assign_filter = me.filter_list.get_filter("status");
			assign_filter && assign_filter.remove(true);

			me.filter_list.add_filter(me.doctype, "status", 'in', "New,Fixing,Fixed");
			me.run();
		}, ".assigned-to-me");
	},
	add_fields: ["task", "task_type"],
}
