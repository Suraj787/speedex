# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
def execute(filters=None):
    columns, data = [], []
    
    columns = get_columns()
    get_ss_details = get_salary_slip_entries(filters)
    format="%d/%m/%Y"
    if get_ss_details:
        for ss in get_ss_details:
        	data.append([ss.name,ss.supplier,ss.customer,ss.ref_no,ss.grand_total,ss.posting_date])

    #frappe.throw(str(columns))
    return columns, data

def get_columns():
    return [
    _("SERIES") + ":Link/Purchase Invoice:150",
    _("SUPPLIER NAME") + ":Link/Supplier:250",
    _("CUSTOMER") + ":Link/Customer:250",
    _("REF NO") + ":Data:100",
    _("GRAND TOTAL") + ":Currency:150",
    _("DATE") + ":Date:150"
    ]

def get_salary_slip_entries(filters):
    return frappe.db.sql("""SELECT `tabPurchase Invoice`.name, `tabPurchase Invoice`.supplier, `tabPurchase Invoice`.customer_name, `tabPurchase Invoice`.ref_no, `tabPurchase Invoice`.grand_total,`tabPurchase Invoice`.posting_date
        FROM `tabPurchase Invoice`
        {salary_slip_conditions} 
        ORDER BY `tabPurchase Invoice`.posting_date desc, `tabPurchase Invoice`.name desc"""\
        .format(salary_slip_conditions=get_salary_slip_conditions(filters)), filters, as_dict=1)

    
def get_salary_slip_conditions(filters):
        conditions = []
        if filters.get("company"):
            conditions.append("`tabPurchase Invoice`.company=%(company)s")
        if filters.get("customer"):
            conditions.append("`tabPurchase Invoice`.customer_name = %(customer)s")
        if filters.get("from_date"):
            conditions.append("`tabPurchase Invoice`.posting_date >= %(from_date)s")
        if filters.get("to_date"):
            conditions.append("`tabPurchase Invoice`.posting_date <= %(to_date)s")
        if filters.get("ref_no"):
            conditions.append("`tabPurchase Invoice`.ref_no = %(ref_no)s")

        conditions.append("`tabPurchase Invoice`.docstatus = 1")
        conditions.append("`tabPurchase Invoice`.naming_series = 'DN-.####'")
        return "WHERE {}".format(" and ".join(conditions)) if conditions else ""
