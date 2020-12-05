from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
	config =  [
		{
			"label": _("Third Party Payments"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Third Party Payments",
					"doctype": "Purchase Invoice",
				},
			]
		},

	]

	return config