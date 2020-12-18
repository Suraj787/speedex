import frappe

def validate(doc,method):
    if doc.naming_series=="SPX-DN.-.####":
        for d in doc.get('items'):
            account=frappe.db.get_value('Item',d.item_code,'gl_entry__account_of_api')
            if account:
                d.income_account=account