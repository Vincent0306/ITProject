import json
import xml.etree.ElementTree as ET
import requests
from time import sleep
from pprint import pprint
import datetime
import re
import os

# transfer date
def convert_timestamp_to_date(timedata):
    
    if isinstance(timedata, str) and timedata.startswith('/Date('):
        timedata = int(timedata.replace('/Date(', '').replace(')/', '').split('+')[0])
    elif isinstance(timedata, str) and timedata.isdigit():
        timedata = int(timedata)
    elif isinstance(timedata, str):  
        return timedata
    
    return datetime.datetime.fromtimestamp(timedata / 1000, tz=datetime.timezone.utc).strftime('%Y-%m-%d')

## transferpdf to json invoice
def transfer_json(data):

    converted_data = {
        "_D": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        "_S": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "_B": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        "Invoice": [{
            "CustomizationID": [{
                "IdentifierContent": "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0"
            }],
            "ProfileID": [{
                "IdentifierContent": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
            }],
            "Approver": [{"TextContent": data['Form_data']['approver']}],
            "Approver_email": [{"TextContent": data['Form_data']['approver_email']}],
            "BPayRef": [{"TextContent": data['Form_data']['bPayRef']}],
            "BPaycode": [{"TextContent": data['Form_data']['bPaycode']}],

            "ID": [{"IdentifierContent": data['invoiceForm']['invoiceNumber']}],
            "IssueDate": [{"DateContent": convert_timestamp_to_date(data['invoiceForm']['invoiceDate'])}],  
            "InvoiceTypeCode": [{
                "IdentifierContent": "380"
            }],
            
            "Note": [{
                "TextContent": "Tax invoice"
            }],

            "DocumentCurrencyCode": [{
                "IdentifierContent": "AUD"
            }],
            "AccountingCost": [{
                "TextContent": data['Form_data']['glcode_text']
            }],

            "OrderReference": [{
                "ID": [{
                    "IdentifierContent": "PurchaseOrderReference"
                }],
                "SalesOrderID": [{
                    "IdentifierContent": data['invoiceForm']['purchaseOrder']
                }]
            }],

            "AccountingSupplierParty": [{
                "Party": [{
                    "EndpointID": [{
                        "IdentifierContent": data['invoiceForm']['ABNnumber'], "schemeID": "0151"
                        }],
                    "PartyIdentification": [{
                        "ID": [{
                            "IdentifierContent": data['Form_data']['supplier_id']
                            }]
                        }],
                    
                    "PartyName": [{
                        "Name": [{
                            "TextContent": data['invoiceForm']['supplierName']
                            }]
                        }],
                
                    "PostalAddress": [{
                        "StreetName": [{
                            "TextContent": data['Form_data']['supplier_address']['1']
                            }], 
                        "AdditionalStreetName": [{
                            "TextContent": data['Form_data']['supplier_address']['0']
                            }],
                        "CityName": [{
                            "TextContent": data['Form_data']['supplier_address']['2']['0']
                            }], 
                        "PostalZone": [{
                            "TextContent": data['Form_data']['supplier_address']['2']['1']
                            }], 

                        "Country": [{
                            "IdentificationCode": [{
                                "IdentifierContent": "AU"
                                }]
                            }]
                        }],
                    "PartyTaxScheme": [{
                       
                        "CompanyID": [{
                            "IdentifierContent": data['invoiceForm']['ABNnumber']
                            }],
                        "TaxScheme": [{
                            "ID": [{
                                "TextContent": "GST"
                                }]
                            }]
                        }],
                    "PartyLegalEntity": [{
                        "RegistrationName": [{
                            "TextContent": data['invoiceForm']['supplierName']
                            }],
                        "CompanyID": [{
                            "IdentifierContent": data['invoiceForm']['ABNnumber'], "schemeID": "0151"
                            }],
                        }],
                    "Contact": [{
                        "Name": [{
                            "TextContent": data['invoiceForm']['supplierName']
                            }],
                        "Telephone": [{
                            "TextContent": data['Form_data']['supplier_address']['3']
                            }], 
                        "ElectronicMail": [{
                            "TextContent": data['Form_data']['email']
                        }] 
                    }]
                }]
            }],

            "AccountingCustomerParty": [{
                "Party": [{
                    "EndpointID": [{
                        "IdentifierContent": "Please Enter Customer ID (ABN)", "schemeID": "0151"
                    }],
                    "PartyIdentification": [{
                        "ID": [{
                            "IdentifierContent": "Please Enter Customer ID (ABN)", "schemeID": "0151"
                        }]
                    }],
                    "PartyName": [{
                        "Name": [{
                            "TextContent": data['Form_data']['invoice_to_address']['1']
                        }]
                    }],
                    "PostalAddress": [{
                        "StreetName": [{
                            "TextContent": data['Form_data']['invoice_to_address']['2']
                        }],
                        "AdditionalStreetName": [{
                            "TextContent": data['Form_data']['invoice_to_address']['2']
                        }],
                        "CityName": [{
                            "TextContent": data['Form_data']['invoice_to_address']['3']['0'].split()[1]
                        }],
                        "PostalZone": [{
                            "TextContent": data['Form_data']['invoice_to_address']['3']['1']
                        }],
                        "Country": [{
                            "IdentificationCode": [{
                                "IdentifierContent": "AU"
                            }]
                        }]
                    }],
                    "PartyTaxScheme": [{
                        "CompanyID": [{
                            "IdentifierContent": "Please Enter Customer ID (ABN)"
                        }],
                        "TaxScheme": [{
                            "ID": [{
                                "IdentifierContent": "GST"
                            }]
                        }]
                    }],
                    "PartyLegalEntity": [{
                        "RegistrationName": [{
                            "TextContent": data['Form_data']['invoice_to_address']['1']
                        }],
                        "CompanyID": [{
                            "IdentifierContent": "Please Enter Customer ID (ABN)", "schemeID": "0151"
                            
                        }]
                    }],
                    "Contact": [{
                        "ElectronicMail": [{
                            "TextContent": data['Form_data']['email_to']
                        }]
                    }]
                }]
            }],

            "PayeeParty": [{ 
                "PartyIdentification": [{
                    "ID": [{
                        "IdentifierContent": "Please Enter Customer ID (ABN)"
                    }]
                }],
                "PartyName": [{
                    "Name": [{
                        "TextContent":data['Form_data']['invoice_to_address']['1'] ## 
                    }]
                }],
                "PartyLegalEntity": [{
                    "CompanyID": [{
                        "IdentifierContent": "Please Enter Customer ID (ABN)", "schemeID": "0151"
                       
                    }]
                }]
            }],

            "Delivery": [{
                "ActualDeliveryDate": [{
                    "DateContent":  convert_timestamp_to_date(data['invoiceForm']['invoiceDate'])
                }],
                "DeliveryLocation": [{
                    "ID": [{
                        "IdentifierContent": "Please Enter Customer ID (ABN)", "schemeID": "0151" #customer ABN
                    }],
                    "Address": [{
                        "StreetName": [{
                            "TextContent": data['Form_data']['delivery_to_address']['2']
                        }],
                        "AdditionalStreetName": [{
                            "TextContent": data['Form_data']['delivery_to_address']['2']
                        }],
                        "CityName": [{
                            "TextContent": data['Form_data']['delivery_to_address']['3']['0'][1]
                        }],
                        "PostalZone": [{
                            "TextContent": data['Form_data']['delivery_to_address']['3']['1']
                        }],
                        "CountrySubentity": [{
                            "TextContent": data['Form_data']['delivery_to_address']['3']['0'][2]
                        }],
                        "Country": [{
                            "IdentificationCode": [{
                                "IdentifierContent": "AU"
                            }]
                        }]
                    }]
                }]
            }],

            "PaymentMeans": [{
                "PaymentMeansCode": [{
                    "IdentifierContent": "30", "name":"Credit transfer"}], 
                "PaymentID": [{"IdentifierContent": data['invoiceForm']['bankReference']}],
                "PayeeFinancialAccount": [{
                    "ID": [{"IdentifierContent": "Please Enter your account number for payment"}],
                    "Name": [{"TextContent": data['Form_data']['bank_details']}],
                    "FinancialInstitutionBranch": [{
                        "ID": [{"IdentifierContent": data['invoiceForm']['bankBranch']}]
                        }]
                    }]
            }],
            "PaymentTerms": [{
            "Note": [{
                "TextContent": "Please Enter your PaymentTerms"
                }]
            }],
            "AllowanceCharge": [{
                "ChargeIndicator": [{
                    "IdentifierContent": str(data['Form_data']['changed']).lower() ##true
                }],
                "AllowanceChargeReasonCode": [{
                    "IdentifierContent": data['Form_data']['description']
                }],
                "AllowanceChargeReason": [{
                    "TextContent": "Discount"
                }],
                "MultiplierFactorNumeric": [{
                    "NumericContent": "0"  
                }],
                "Amount": [{ 
                    "AmountContent": "0", "currencyID": "AUD"
                }],
                "BaseAmount": [{
                    "AmountContent": "0", "currencyID": "AUD"
                }],
                "TaxCategory": [{
                    "ID": [{
                        "IdentifierContent": "S"
                    }],
                    "Percent": [{
                        "NumericContent": round(float(data['invoiceForm']['gstTotal']) / float(data['invoiceForm']['subTotal']), 2) * 100
                    }],
                    "TaxScheme": [{
                        "ID": [{
                            "IdentifierContent": "GST"
                            }]
                        }]
                }]
            }],
            "TaxTotal": [{
                "TaxAmount": [{
                    "AmountContent": data['invoiceForm']['gstTotal'], "currencyID": "AUD"
                }],
                "TaxSubtotal": [{
                    "TaxableAmount": [{
                        "AmountContent": data['invoiceForm']['subTotal'], "currencyID": "AUD"
                    }],
                    "TaxAmount": [{
                        "AmountContent": data['invoiceForm']['gstTotal'], "currencyID": "AUD"
                    }],
                    "TaxCategory": [{
                        "ID": [{
                            "IdentifierContent": "S"
                        }],
                        "Percent": [{
                            "NumericContent": round(float(data['invoiceForm']['gstTotal']) / float(data['invoiceForm']['subTotal']), 2) * 100
                        }],
                        "TaxScheme": [{
                            "ID": [{
                                "IdentifierContent": "GST"
                            }]
                        }]
                    }]
                }]
            }], 
            "LegalMonetaryTotal": [{
                "LineExtensionAmount": [{
                    "AmountContent": data['invoiceForm']['subTotal'], "currencyID": "AUD"
                }],
                "TaxExclusiveAmount": [{
                    "AmountContent": data['invoiceForm']['subTotal'], "currencyID": "AUD"
                }],
                "TaxInclusiveAmount": [{
                    "AmountContent": data['invoiceForm']['invoiceTotal'], "currencyID": "AUD"
                }],
                "ChargeTotalAmount": [{
                    "AmountContent": data['invoiceForm']['chargeTotal'], "currencyID": "AUD"
                }],
                "PrepaidAmount": [{
                    "AmountContent": data['invoiceForm']['chargeTotal'], "currencyID": "AUD"
                }],
                "PayableAmount": [{
                    "AmountContent": data['invoiceForm']['invoiceTotal'], "currencyID": "AUD"
                }]
             }],
                "InvoiceLine": []
        }]
    }

    #invoiceLine
    def unicode_get(item_input):
        if item_input == "EACH" or item_input == '':
            return "E99"
        elif item_input == "DAY":
            return "DAY"
        else:
            return item_input
        
    ##for invoice_line ID: line number
    i = 1
    for item in data['Table']:
        invoice_line = {
            "ID": [{"IdentifierContent": i}],
            "Note": [{
                    "TextContent": "Invoice Line Description"
                }],
            "InvoicedQuantity": [{
                    "NumericContent": item['quantity'], 
                    "unitCode": unicode_get(item['unit_measure'])
                }],
            "LineExtensionAmount": [{
                    "AmountContent": round(item['unit_price'], 2), 
                    "currencyID":"AUD"
                }],
           "AccountingCost": [{
                    "TextContent": item['gl_code']
                }],

            "Item": [{
                "Description": [{"TextContent": item['description']}],
                "Name": [{
                        "TextContent": item['description'].split()[0]
                    }],
                "SellersItemIdentification": [{
                        "ID": [{
                            "IdentifierContent": item['article_code']
                        }]
                    }],
                "StandardItemIdentification": [{
                        "ID": [{
                            "IdentifierContent": item['article_code'], "schemeID": "0151"
                        }]
                    }],
                "OriginCountry": [{
                        "IdentificationCode": [{
                            "IdentifierContent": "AU"
                        }]
                    }],
                "ClassifiedTaxCategory": [{
                        "ID": [{
                            "IdentifierContent": "S"
                        }],
                        "Percent": [{
                            "NumericContent": round(float(data['invoiceForm']['gstTotal']) / float(data['invoiceForm']['subTotal']), 2) * 100
                        }],
                        "TaxScheme": [{
                            "ID": [{
                                "IdentifierContent": "GST"
                            }]
                        }]
                    }]
                }],
            "Price": [{
                    "PriceAmount": [{
                        "AmountContent": round(float(item['unit_price']) / float(item['quantity']), 2), "currencyID":"AUD"
                    }],
                  
                    "AllowanceCharge": [{
                        "ChargeIndicator": [{
                            "IdentifierContent": "false"
                        }],
                        "Amount": [{
                            "AmountContent": '0', "currencyID":"AUD"
                        }],
                        "BaseAmount": [{
                            "AmountContent": round(item['unit_price'], 2), "currencyID":"AUD" #4.57
                        }]
                    }]
                }]
        }
        converted_data["Invoice"][0]["InvoiceLine"].append(invoice_line)
        i += 1

    return json.dumps(converted_data, indent=4)


## Transfer pdf to json, use transform_to_xml to transfer json to xml
def pdf_to_json(file_path):
    
   #Set up variables
    url = 'https://app.ezzydoc.com/EzzyService.svc/Rest'
    api_key = {'APIKey': '30f13f6b-8e6b-4a7e-80c5-2463b08a9287'}
    payload = {'user': 'Xiyu',
            'pwd': 'huWJ562@',
            'APIKey': '30f13f6b-8e6b-4a7e-80c5-2463b08a9287'}

    # Log in to EzzyBills
    r = requests.get(url + '/Login', params=payload)

    #Upload an invoice to EzzyBills
    with open(file_path, 'rb') as img_file:
        data_input = img_file.read()
        b = bytearray(data_input)
        li = []
        for i in b:
            li.append(i)

        file_name = os.path.basename(file_path)
        raw_data = {"PictureName": file_name, "PictureStream": li}
        json_data = json.dumps(raw_data)
        #upload the invoice to EzzyBills 
        r1 = requests.post("https://app.ezzydoc.com/EzzyService.svc/Rest/uploadInvoiceImage",
                        data=json_data,
                        cookies=r.cookies,
                        params=api_key,
                        headers={'Content-Type': 'application/json'})
        invoiceID = str(r1.json().get("invoice_id"))
    

    #Wait until invoice has been processed
    completeBool = False
    while True:
        r2 = requests.get(url + '/workflowStatus?invoiceid=' + invoiceID,
                            cookies=r.cookies,
                            params=api_key)
      
        state = r2.json().get("state")
     
        if state == 24 or state == 26:
            completeBool = True
        if completeBool == True:
            break
        sleep(1)

    r3 = requests.get(url + '/getFormData?invoiceid=' + invoiceID,
                    cookies=r.cookies,
                    params=api_key)

    r4 = requests.get(url + '/getInvoiceHeaderBlocks?invoiceid=' + invoiceID,
                    cookies=r.cookies,
                    params=api_key)

    r3_json =  r3.json()

    del r3_json['form_data']['abn']
    del r3_json['form_data']['bankAccount']
    del r3_json['form_data']['bankBranch']
    del r3_json['form_data']['charge']
    del r3_json['form_data']['document_subtype']
    del r3_json['form_data']['tax']
    del r3_json['form_data']['invoiceDate']
    del r3_json['form_data']['invoiceNumber']
    del r3_json['form_data']['total']
    del r3_json['form_data']['purchaseOrder']
    del r3_json['form_data']['supplier']

   
    ## deal with supplier address
    addresses = {}
    citypost = {}
    supplier_address = r3_json['form_data']['supplier_address']
    if supplier_address:
        supplier_address_list = supplier_address.split('\r\n')
        for i in range(len(supplier_address_list)-1):
            addresses[i] = supplier_address_list[i]
    
        if addresses[2]:
            add2 = re.match(r'^(.*?)(\d+)$', addresses[2])
            if add2:
                citypost['0'] = add2.group(1).strip()
                citypost['1'] = add2.group(2)

        addresses[2] = citypost
    r3_json['form_data']['supplier_address'] = addresses

    ##deal with delivery_to_address
    delivery_to_address = r3_json['form_data']['delivery_to_address']
    if delivery_to_address:
        delivery_addresses = {}
        delivery_citypost = {}
        delivery_to_address_list = delivery_to_address.split('\r\n')
        for j in range(len(delivery_to_address_list)-1):
            delivery_addresses[j] = delivery_to_address_list[j] ##do not get k=0
    
        if delivery_addresses[3]:
            deliver_add3 = re.match(r'^(.*?)(\d+)$', delivery_addresses[3])
            if deliver_add3:
                delivery_citypost['0'] = deliver_add3.group(1).strip().split()
                delivery_citypost['1'] = deliver_add3.group(2)

        delivery_addresses[3] = delivery_citypost
    r3_json['form_data']['delivery_to_address'] = delivery_addresses

    ## invoice_to_address
    invoice_to_address = r3_json['form_data']['invoice_to_address']
    if invoice_to_address:
        invoice_addresses = {}
        invoice_citypost = {}
        invoice_to_address_list = invoice_to_address.split('\r\n')
        for k in range(len(invoice_to_address_list)-1):
            invoice_addresses[k] = invoice_to_address_list[k] ##do not get k=0
    
        if invoice_addresses[3]:
            invoice_add3 = re.match(r'^(.*?)(\d+)$', invoice_addresses[3])
            if invoice_add3:
                invoice_citypost['0'] = invoice_add3.group(1).strip()
                invoice_citypost['1'] = invoice_add3.group(2)

        invoice_addresses[3] = invoice_citypost
    r3_json['form_data']['invoice_to_address'] = invoice_addresses

    r3._content = json.dumps(r3_json).encode('utf-8')

    r4_json =  r4.json()
    r4_json['invoiceForm']['invoiceDate'] = r4_json['invoiceForm']['paymentDate']
    r4._content = json.dumps(r4_json).encode('utf-8')

    #generate a json file with used data
    data = {
        "Form_data": r3.json()['form_data'],
        "Locale": r3.json()['locale'], ## issue place
        "invoiceForm": r4.json()['invoiceForm'],
        "Table": r4.json()['table'],
        "Service_status": r4.json()['service_status'],

    }

    transferred_json = transfer_json(data)
    
    return transferred_json


def handle_dict_to_xml(parent, key, value):
    if isinstance(value, list):
        sub_elem = None
        for item in value:
            if isinstance(item, dict):
                sub_elem = ET.SubElement(parent, key)
                for sub_key, sub_value in item.items():
                    if sub_value not in [None, "", "null"]:
                        handle_dict_to_xml(sub_elem, sub_key, sub_value)

                #delete if sub_element is Null
                if sub_elem is not None and not list(sub_elem):
                    parent.remove(sub_elem)
            elif item not in [None, "", "null"]:
                sub_elem = ET.SubElement(parent, key)
                sub_elem.text = str(item)
    elif isinstance(value, dict):
        sub_elem = ET.SubElement(parent, key)
        for sub_key, sub_value in value.items():
            if sub_value not in [None, "", "null"]:
                handle_dict_to_xml(sub_elem, sub_key, sub_value)

       #delete if sub_element is Null
        if not list(sub_elem):
            parent.remove(sub_elem)
    else:
        if value not in [None, "", "null"]:
            sub_elem = ET.SubElement(parent, key)
            sub_elem.text = str(value)


# Transform json to xml
def transform_to_xml(json_data):
    root = ET.Element("Invoice")

    for key, val in json_data.items():
        if key.startswith("_"):
            continue
        handle_dict_to_xml(root, key, val)

    return root
