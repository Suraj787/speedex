from __future__ import unicode_literals
import requests
import frappe
import json

# bench execute speedex.dump_data.data_entry
def data_entry():
    ref_list = []
    r = requests.get('https://speedexlogistics.com/s/api/accounts/sea/cheque_payment/list.php',
    headers={'sessionID': '1'}) 
    op=r.content
    if type(r.content)==bytes:
       op=(r.content).decode("utf-8")
    item_list = json.loads(op)
    all_pi = frappe.get_all("Purchase Invoice", ["ref_no"])
    for pi in all_pi:
        ref_list.append(pi.get('ref_no')) 
    for item in item_list:
        if item.get('ref') not in ref_list:
            ref_list.append(item.get('ref'))
            pi_doc = frappe.get_doc({
                "doctype" : "Purchase Invoice",
                "company" : "Speedex Logistics Limited",
                "supplier" : "Government",
                "client_id" : item.get('client_id'),
                "ref_no" : item.get('ref'),
                "sea_id" : item.get('sea_id'),

            })
            for i in item.get('items'):
                for my_item in i.keys():
                    q = "select expense_account from `tabItem Default` where parent ='{0}';".format(my_item)
                    expense_acc = frappe.db.sql(q)
                    pi_doc.append("items",{
                        "item_name": my_item,
                        "qty" : 1,
                        "expense_account" :expense_acc[0][0] if expense_acc and expense_acc[0][0] else "Administrative Expenses - SLL" ,
                        "uom" : "Nos",
                        "rate":i[my_item]
                    })
            pi_doc.insert()
            pi_doc.submit()
    return 'OK'

# bench execute speedex.dump_data.payment_entry
def payment_entry():
    ref_list = []
    r = requests.get('https://speedexlogistics.com/s/api/accounts/sea/cheque_payment/cheque_payment_entries.php',
    headers={'sessionID': '1'}) 
    op=r.content
    if type(r.content)==bytes:
       op=(r.content).decode("utf-8")
    item_list = json.loads(op)
    all_pi = frappe.get_all("Payment Entry", ["ref_no"])
    import datetime
    for pi in all_pi:
        ref_list.append(pi.get('ref')) 
    for item in item_list:
        if item.get('ref') not in ref_list:
            ref_list.append(item.get('ref'))
            datetime_obj = datetime.datetime.strptime(item.get('date_opened'), '%d/%m/%Y')
            for d in frappe.get_all('Purchase Invoice',{'ref_no':item.get('ref')},['name','supplier','due_date']):
                pe_doc = frappe.get_doc({
                    "doctype" : "Payment Entry",
                    "payment_type":"Pay",
                    "posting_date":datetime_obj.date(),
                    "mode_of_payment":"Cheque",
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
                    "total_amount":item.get('Total_Amount'),
                    "allocated_amount":item.get('Total_Amount')
                })
                pe_doc.insert()
                pe_doc.submit()
    return 'OK'



# delete all purchase invoices

# bench execute speedex.dump_data.delete_purchase_invoices
def delete_purchase_invoices():
    for d in frappe.get_all('Purchase Invoice',['name','docstatus']):
        doc=frappe.get_doc('Purchase Invoice',d.name)
        print(doc.name)
        if d.docstatus==1:
            doc.cancel()
        frappe.delete_doc("Purchase Invoice",doc.name)



# delete all payment entries

# bench execute speedex.dump_data.delete_payment_entry
def delete_payment_entry():
    for d in frappe.get_all('Payment Entry',['name','docstatus']):
        doc=frappe.get_doc('Payment Entry',d.name)
        print(doc.name)
        if d.docstatus==1:
            doc.cancel()
        frappe.delete_doc("Payment Entry",doc.name)
