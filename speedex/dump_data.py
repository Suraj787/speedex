from __future__ import unicode_literals
import requests
import frappe
import json

@frappe.whitelist()
def data_entry():
    sea_list = []
    r = requests.get('https://speedexlogistics.com/s/api/accounts/sea/cheque_payment/list.php',
    headers={'sessionID': '1'}) 
    item_list = json.loads(r.content)
    all_pi = frappe.get_all("Purchase Invoice", ["sea_id"])
    for pi in all_pi:
        sea_list.append(pi.get('sea_id'))
    for item in item_list:
        if item.get('sea_id') not in sea_list:
            pi_doc = frappe.get_doc({
                "doctype" : "Purchase Invoice",
                "company" : "erpnext",
                "supplier" : "Goverment",
                "client_id" : item.get('client_id'),
                "ref_no" : item.get('ref_no'),
                "sea_id" : item.get('sea_id'),

            })
            for i in item.get('items'):
                for my_item in i.keys():
                    pi_doc.append("items",{
                        "item_name": my_item,
                        "qty" : 1,
                        "expense_account" : "Stock Received But Not Billed - E",
                        "uom" : "Nos",
                    })
            pi_doc.insert()
            pi_doc.submit()
    return 'OK'