from __future__ import unicode_literals
import requests
import frappe
import json

# bench execute speedex.dump_data.data_entry
def data_entry():
    ref_list = []
    r = requests.get('https://speedexlogistics.com/s/api/accounts/sea/cheque_payment/list.php',
    headers={'sessionID': '1'}) 
#     print(r.content)
#     print(type(r.content))
    op=r.content
    if type(r.content)==bytes:
       op=(r.content).decode("utf-8")
    item_list = json.loads(op)
    print(item_list)
#     all_pi = frappe.get_all("Purchase Invoice", ["ref_no"])
#     for pi in all_pi:
#         ref_list.append(pi.get('ref_no')) 
#     for item in item_list:
#         if item.get('ref') not in ref_list:
#             pi_doc = frappe.get_doc({
#                 "doctype" : "Purchase Invoice",
#                 "company" : "Speedex Logistics Limited",
#                 "supplier" : "Government",
#                 "client_id" : item.get('client_id'),
#                 "ref_no" : item.get('ref'),
#                 "sea_id" : item.get('sea_id'),

#             })
#             for i in item.get('items'):
#                 for my_item in i.keys():
#                     pi_doc.append("items",{
#                         "item_name": my_item,
#                         "qty" : 1,
#                         "expense_account" :"Administrative Expenses - SLL" ,
#                         "uom" : "Nos",
#                     })
#             pi_doc.insert()
#             pi_doc.submit()
#     return 'OK'

# bench execute speedex.dump_data.payment_entry
def payment_entry():
    ref_list = []
    r = requests.get('https://speedexlogistics.com/s/api/accounts/sea/cheque_payment/cheque_payment_entries.php',
    headers={'sessionID': '1'}) 
    item_list = json.loads(r.content)
    all_pi = frappe.get_all("Payment Entry", ["ref_no"])
    import datetime
    for pi in all_pi:
        ref_list.append(pi.get('ref')) 
    for item in item_list:
        if item.get('ref') not in ref_list:
            datetime_obj = datetime.datetime.strptime(item.get('date_opened'), '%d/%m/%Y')
            for d in frappe.get_all('Purchase Invoice',{'ref_no':item.get('ref')},['name','supplier','due_date']):
                pe_doc = frappe.get_doc({
                    "doctype" : "Payment Entry",
                    "payment_type":"Pay",
                    "posting_date":datetime_obj.date(),
                    "mode_of_payment":"Cash",
                    "party_type":"Supplier",
                    "ref_no" : item.get('ref'),
                    "party":d.get('supplier'),
                    "paid_amount":item.get('Total_Amount'),
                    "paid_from":"I&M - SLL",
                    "received_amount":float(item.get('Total_Amount')),
                    "reference_no":item.get('cheque_no'),
                    "reference_date":datetime_obj.date()
                })
                pe_doc.append("references",{
                    "reference_doctype": 'Purchase Invoice',
                    "reference_name":d.name,
                    "due_date":d.due_date,
                    "total_amount":item.get('Total_Amount')
                })
                pe_doc.insert()
                pe_doc.submit()
    return 'OK'
