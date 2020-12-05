frappe.listview_settings['Purchase Invoice'] = {
	onload: function (listview) {
		frappe.route_options = {"name": ["not like", "DN%"]};
	},
};
