import json
import xml.etree.ElementTree as ET

def get_text_from_elements(root, path):
        elements = root.findall(path)
        return [el.text.strip() for el in elements if el is not None and el.text and el.text.strip()]


def get_text_from_element(root, path):
    element = root.find(path)
    if element is not None and element.text and element.text.strip():
        return element.text.strip()
    return None


# Transform xml (field is not empty) to ubl 2.1
def transform_to_ubl(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Define namespaces
    NSMAP = {
        'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
        }

    # Register namespaces
    for prefix, uri in NSMAP.items():
        ET.register_namespace(prefix, uri)

    # Create the UBL structure
    ubl_root = ET.Element('Invoice',{'xmlns':"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"})
   
    # Add ext:UBLExtensions
    approver_text = get_text_from_element(root, './/Approver/TextContent')
    approver_email_text = get_text_from_element(root, './/ApproverEmail/TextContent')
    bpay_ref_text = get_text_from_element(root, './/BPayRef/TextContent')
    bpay_code_text = get_text_from_element(root, './/BPaycode/TextContent')

   # Add custom fields in ExtensionContent
    if approver_text or approver_email_text or bpay_ref_text or bpay_code_text:
        ext_ubl_extensions = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}UBLExtensions')
        ext_ubl_extension = ET.SubElement(ext_ubl_extensions, '{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}UBLExtension')
        ext_extension_content = ET.SubElement(ext_ubl_extension, '{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}ExtensionContent')

        if approver_text:
            approver = ET.SubElement(ext_extension_content, 'Approver')
            approver.text = approver_text

        if approver_email_text:
            approver_email = ET.SubElement(ext_extension_content, 'ApproverEmail')
            approver_email.text = approver_email_text

        if bpay_ref_text:
            bpay_ref = ET.SubElement(ext_extension_content, 'BPayRef')
            bpay_ref.text = bpay_ref_text

        if bpay_code_text:
            bpay_code = ET.SubElement(ext_extension_content, 'BPaycode')
            bpay_code.text = bpay_code_text

    customization_id_text = get_text_from_element(root, './/CustomizationID/IdentifierContent')
    profile_id_text = get_text_from_element(root, './/ProfileID/IdentifierContent')

    if customization_id_text:
        cbc_customization_id = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CustomizationID')
        cbc_customization_id.text = customization_id_text

    if profile_id_text:
        cbc_profile_id = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ProfileID')
        cbc_profile_id.text = profile_id_text

    # ID
    id_text = get_text_from_element(root, './/ID/IdentifierContent')
    if id_text:
        cbc_id = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cbc_id.text = id_text

    # IssueDate
    issue_date = get_text_from_element(root, './/IssueDate/DateContent')
    if issue_date:
        cbc_issue_date = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate')
        cbc_issue_date.text = issue_date

    ## DueDate
    due_date = get_text_from_element(root, './/DueDate/DateContent')
    if due_date:
        cbc_due_date = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DueDate')
        cbc_due_date.text = due_date

    #InvoiceTypeCode
    invoice_type_code = get_text_from_element(root, './/InvoiceTypeCode/IdentifierContent')
    if not invoice_type_code:
        invoice_type_code = "380"  # default value

    cbc_invoice_type_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoiceTypeCode')
    cbc_invoice_type_code.text = invoice_type_code

    #Note
    note = get_text_from_element(root, './/Note/TextContent')
    if note:
        cbc_note = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Note')
        cbc_note.text = note

    ## TaxPointDate
    tax_point_date = get_text_from_element(root, './/TaxPointDate/DateContent')
    if tax_point_date:
        cbc_tax_point_date = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxPointDate')
        cbc_tax_point_date.text = tax_point_date

    #DocumentCurrencyCode
    document_currency_code = get_text_from_element(root, './/DocumentCurrencyCode/IdentifierContent')
    if document_currency_code:
        document_currency_code = "AUD"  # default value

        cbc_document_currency_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DocumentCurrencyCode')
        cbc_document_currency_code.text = document_currency_code

    #TaxCurrencyCode
    tax_currency_code = get_text_from_element(root, './/TaxCurrencyCode/IdentifierContent')
    if tax_currency_code:
        tax_currency_code = "AUD"  # default value

        cbc_tax_currency_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxCurrencyCode')
        cbc_tax_currency_code.text = tax_currency_code

    #PricingCurrencyCode
    pricing_currency_code = get_text_from_element(root, './/PricingCurrencyCode/IdentifierContent')
    if pricing_currency_code:
        pricing_currency_code = "AUD"  # default value

        cbc_pricing_currency_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PricingCurrencyCode')
        cbc_pricing_currency_code.text = pricing_currency_code

    #PaymentCurrencyCode
    payment_currency_code = get_text_from_element(root, './/PaymentCurrencyCode/IdentifierContent')
    if payment_currency_code:
        payment_currency_code = "AUD"  # default value

        cbc_payment_currency_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentCurrencyCode')
        cbc_payment_currency_code.text = payment_currency_code

    #PaymentAlternativeCurrencyCode
    payment_alternative_currency_code = get_text_from_element(root, './/PaymentAlternativeCurrencyCode/IdentifierContent')
    if payment_alternative_currency_code:
        payment_alternative_currency_code = "AUD"  # default value

        cbc_payment_alternative_currency_code = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentAlternativeCurrencyCode')
        cbc_payment_alternative_currency_code.text = payment_alternative_currency_code

    #AccountingCost
    accounting_cost = get_text_from_element(root, './/AccountingCost/TextContent')
    if accounting_cost:
        cbc_accounting_cost = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AccountingCost')
        cbc_accounting_cost.text = accounting_cost

    ##BuyerReference
    buyer_reference = get_text_from_element(root, './/BuyerReference/TextContent')
    if buyer_reference:
        cbc_buyer_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}BuyerReference')
        cbc_buyer_reference.text = buyer_reference

    # InvoicePeriod
    start_date = get_text_from_element(root, './/InvoicePeriod/StartDate/DateContent')
    end_date = get_text_from_element(root, './/InvoicePeriod/EndDate/DateContent')
    if start_date or end_date:
        cac_invoice_period = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoicePeriod')
        if start_date:
            cbc_start_date = ET.SubElement(cac_invoice_period, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StartDate')
            cbc_start_date.text = start_date
        if end_date:
            cbc_end_date = ET.SubElement(cac_invoice_period, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndDate')
            cbc_end_date.text = end_date


    # OrderReference
    order_reference_id = get_text_from_element(root, './/OrderReference/ID/IdentifierContent')
    sales_order_id = get_text_from_element(root, './/OrderReference/SalesOrderID/IdentifierContent')
    if order_reference_id or sales_order_id:
        cac_order_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}OrderReference')
        if order_reference_id:
            cbc_order_reference_id = ET.SubElement(cac_order_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            cbc_order_reference_id.text = order_reference_id
        if sales_order_id:
            cbc_sales_order_id = ET.SubElement(cac_order_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}SalesOrderID')
            cbc_sales_order_id.text = sales_order_id


    ##BillingReference-3 level
    bill_reference_id = get_text_from_element(root, './/BillingReference/InvoiceDocumentReference/ID/IdentifierContent')
    bill_issue_date = get_text_from_element(root, './/BillingReference/InvoiceDocumentReference/IssueDate/DateContent')
    if bill_reference_id or bill_issue_date:
        cac_bill_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}BillingReference')
        cac_invoice_document_reference = ET.SubElement(cac_bill_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoiceDocumentReference')
        if bill_reference_id:
            cbc_bill_reference_id = ET.SubElement(cac_invoice_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            cbc_bill_reference_id.text = bill_reference_id
        if bill_issue_date:
            cbc_bill_issue_date = ET.SubElement(cac_invoice_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate')
            cbc_bill_issue_date.text = bill_issue_date


    #DespatchDocumentReference
    despatch_document_reference_id = get_text_from_element(root, './/DespatchDocumentReference/ID/IdentifierContent')
    if despatch_document_reference_id:
        cac_despatch_document_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}DespatchDocumentReference')
        cac_despatch_document_referenc_id = ET.SubElement(cac_despatch_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cac_despatch_document_referenc_id.text = despatch_document_reference_id


    #ReceiptDocumentReference 
    receipt_document_reference_id = get_text_from_element(root, './/ReceiptDocumentReference/ID/IdentifierContent')
    if receipt_document_reference_id:
        cac_receipt_document_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}ReceiptDocumentReference')
        cac_receipt_document_referenc_id = ET.SubElement(cac_receipt_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cac_receipt_document_referenc_id.text = receipt_document_reference_id


    #StatementDocumentReference 
    statement_document_reference_id = get_text_from_element(root, './/StatementDocumentReference/ID/IdentifierContent')
    if statement_document_reference_id:
        cac_statement_document_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}StatementDocumentReference')
        cac_statement_document_referenc_id = ET.SubElement(cac_statement_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cac_statement_document_referenc_id.text = statement_document_reference_id

    #OriginatorDocumentReference 
    originator_document_reference_id = get_text_from_element(root, './/OriginatorDocumentReference/ID/IdentifierContent')
    if originator_document_reference_id:
        cac_originator_document_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}OriginatorDocumentReference')
        cac_originator_document_referenc_id = ET.SubElement(cac_originator_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cac_originator_document_referenc_id.text = originator_document_reference_id


    #ContractDocumentReference  
    contract_document_reference_id = get_text_from_element(root, './/ContractDocumentReference/ID/IdentifierContent')
    if contract_document_reference_id:
        cac_contract_document_reference = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}ContractDocumentReference')
        cac_contract_document_referenc_id = ET.SubElement(cac_contract_document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
        cac_contract_document_referenc_id.text = contract_document_reference_id

    # AccountingSupplierParty
    endpoint_id_text = get_text_from_element(root, './/Party/EndpointID/IdentifierContent')
    sullpier_listID_text =  get_text_from_element(root, './/Party/EndpointID/schemeID')
    
    ## change the order of party_id_identification and party_name
    party_id_text = get_text_from_element(root, './/PartyIdentification/ID/IdentifierContent')
    party_name_text = get_text_from_element(root, './/PartyName/Name/TextContent')
    street_name_text = get_text_from_element(root, './/PostalAddress/StreetName/TextContent')
    additional_street_name_text = get_text_from_element(root, './/PostalAddress/AdditionalStreetName/TextContent')
    city_name_text = get_text_from_element(root, './/PostalAddress/CityName/TextContent')
    postal_zone_text = get_text_from_element(root,  './/PostalAddress/PostalZone/TextContent')
    country_code_text = get_text_from_element(root, './/PostalAddress/Country/IdentificationCode/IdentifierContent')
    company_id_text = get_text_from_element(root, './/PartyTaxScheme/CompanyID/IdentifierContent')
    supplier_tax_scheme_id_text = get_text_from_element(root, './/PartyTaxScheme/TaxScheme/ID/IdentifierContent')
    registration_name_text = get_text_from_element(root, './/PartyLegalEntity/RegistrationName/TextContent')
    legal_entity_company_id_text = get_text_from_element(root, './/PartyLegalEntity/CompanyID/IdentifierContent')
    legal_entity_company_shemeid_text = get_text_from_element(root, './/PartyLegalEntity/CompanyID/schemeID')
    legal_form_text = get_text_from_element(root, './/PartyLegalEntity/CompanyLegalForm/TextContent')
    contact_name_text = get_text_from_element(root, './/Contact/Name/TextContent')
    contact_telephone_text = get_text_from_element(root, './/Contact/Telephone/TextContent')
    contact_email_text = get_text_from_element(root, './/Contact/ElectronicMail/TextContent')

    # Build the XML tree
    if endpoint_id_text or party_name_text or party_id_text or street_name_text or additional_street_name_text or city_name_text or postal_zone_text or country_code_text or company_id_text or supplier_tax_scheme_id_text or registration_name_text or legal_entity_company_id_text or contact_name_text or contact_telephone_text or contact_email_text:
        cac_supplier_party = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty')
        cac_party = ET.SubElement(cac_supplier_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party')

        if endpoint_id_text and sullpier_listID_text:
            cbc_endpoint_id = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndpointID', schemeID=sullpier_listID_text)
            cbc_endpoint_id.text = endpoint_id_text
        elif endpoint_id_text:
            cbc_endpoint_id = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndpointID')
            cbc_endpoint_id.text = endpoint_id_text

        ## change the order of party_id_identification and party_name
        if party_id_text:
            cac_party_identification = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification')
            cbc_id = ET.SubElement(cac_party_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            cbc_id.text = party_id_text

        if party_name_text:
            cac_party_name = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
            cbc_name = ET.SubElement(cac_party_name, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
            cbc_name.text = party_name_text

        if street_name_text or additional_street_name_text or city_name_text or postal_zone_text or country_code_text:
            cac_postal_address = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PostalAddress')

            if street_name_text:
                cbc_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StreetName')
                cbc_street_name.text = street_name_text

            if additional_street_name_text:
                cbc_additional_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AdditionalStreetName')
                cbc_additional_street_name.text = additional_street_name_text

            if city_name_text:
                cbc_city_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName')
                cbc_city_name.text = city_name_text

            if postal_zone_text:
                cbc_postal_zone = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PostalZone')
                cbc_postal_zone.text = postal_zone_text

            if country_code_text:
                cac_country = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country')
                cbc_identification_code = ET.SubElement(cac_country, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
                cbc_identification_code.text = country_code_text

        if company_id_text or supplier_tax_scheme_id_text:
            cac_party_tax_scheme = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme')

            if company_id_text:
                cbc_company_id = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
                cbc_company_id.text = company_id_text

            if supplier_tax_scheme_id_text:
                cac_tax_scheme = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                cbc_id = ET.SubElement(cac_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                cbc_id.text = supplier_tax_scheme_id_text

        if registration_name_text or legal_entity_company_id_text:
            cac_party_legal_entity = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')

            if registration_name_text:
                cbc_registration_name = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
                cbc_registration_name.text = registration_name_text

            if legal_entity_company_id_text and legal_entity_company_shemeid_text:
                cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID', schemeID=legal_entity_company_shemeid_text)
                cbc_company_id.text = legal_entity_company_id_text
            elif legal_entity_company_id_text:
                cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
                cbc_company_id.text = legal_entity_company_id_text

            if legal_form_text:
                cbc_company_legal_form = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyLegalForm')
                cbc_company_legal_form.text = legal_form_text

        if contact_name_text or contact_telephone_text or contact_email_text:
            cac_contact = ET.SubElement(cac_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Contact')

            if contact_name_text:
                cbc_name = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
                cbc_name.text = contact_name_text

            if contact_telephone_text:
                cbc_telephone = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Telephone')
                cbc_telephone.text = contact_telephone_text

            if contact_email_text:
                cbc_electronic_mail = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ElectronicMail')
                cbc_electronic_mail.text = contact_email_text


    # AccountingCustomerParty
    sendpoint_id_text = get_text_from_element(root, './AccountingCustomerParty/Party/EndpointID/IdentifierContent')
    sendpoint_schemeid_text = get_text_from_element(root, './AccountingCustomerParty/Party/EndpointID/schemeID')
    ## change the order of party_id_identification and party_name
    sparty_id_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyIdentification/ID/IdentifierContent')
    sparty_shcemeid_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyIdentification/ID/schemeID')
    
    party_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyName/Name/TextContent')

    street_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/PostalAddress/StreetName/TextContent')
    additional_street_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/PostalAddress/AdditionalStreetName/TextContent')
    city_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/PostalAddress/CityName/TextContent')
    postal_zone_text = get_text_from_element(root,  './AccountingCustomerParty/Party/PostalAddress/PostalZone/TextContent')
    country_code_text = get_text_from_element(root, './AccountingCustomerParty/Party/PostalAddress/Country/IdentificationCode/IdentifierContent')
    company_id_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyTaxScheme/CompanyID/IdentifierContent')
    customer_tax_scheme_id_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme/ID/IdentifierContent')
    registration_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyLegalEntity/RegistrationName/TextContent')
    legal_entity_company_id_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyLegalEntity/CompanyID/IdentifierContent')
    legal_entity_company_shcemeid_text = get_text_from_element(root, './AccountingCustomerParty/Party/PartyLegalEntity/CompanyID/schemeID')
    
    contact_name_text = get_text_from_element(root, './AccountingCustomerParty/Party/Contact/Name/TextContent')
    contact_telephone_text = get_text_from_element(root, './AccountingCustomerParty/Party/Contact/Telephone/TextContent')
    contact_email_text = get_text_from_element(root, './AccountingCustomerParty/Party/Contact/ElectronicMail/TextContent')

    # Build the XML tree
    if sendpoint_id_text or sparty_id_text or party_id_text or street_name_text or additional_street_name_text or city_name_text or postal_zone_text or country_code_text or company_id_text or customer_tax_scheme_id_text or registration_name_text or legal_entity_company_id_text or contact_name_text or contact_telephone_text or contact_email_text:
        cac_customer_party = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty')
        cac_cus_party = ET.SubElement(cac_customer_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party')

        if sendpoint_id_text and sendpoint_schemeid_text:
            cbc_endpoint_id = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndpointID', schemeID=sendpoint_schemeid_text)
            cbc_endpoint_id.text = sendpoint_id_text
        elif sendpoint_id_text:
            cbc_endpoint_id = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndpointID')
            cbc_endpoint_id.text = sendpoint_id_text

        ## change the order of party_id_identification and party_name
        if sparty_id_text and sparty_shcemeid_text:
            cac_party_identification = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification')
            cbc_id = ET.SubElement(cac_party_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', schemeID=sparty_shcemeid_text)
            cbc_id.text = sparty_id_text
        elif sparty_id_text:
            cac_party_identification = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification')
            cbc_id = ET.SubElement(cac_party_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            cbc_id.text = sparty_id_text

        if party_name_text:
            cac_party_name = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
            cbc_name = ET.SubElement(cac_party_name, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
            cbc_name.text = party_name_text

        if street_name_text or additional_street_name_text or city_name_text or postal_zone_text or country_code_text:
            cac_postal_address = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PostalAddress')

            if street_name_text:
                cbc_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StreetName')
                cbc_street_name.text = street_name_text

            if additional_street_name_text:
                cbc_additional_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AdditionalStreetName')
                cbc_additional_street_name.text = additional_street_name_text

            if city_name_text:
                cbc_city_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName')
                cbc_city_name.text = city_name_text

            if postal_zone_text:
                cbc_postal_zone = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PostalZone')
                cbc_postal_zone.text = postal_zone_text

            if country_code_text:
                cac_country = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country')
                cbc_identification_code = ET.SubElement(cac_country, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
                cbc_identification_code.text = country_code_text

        if company_id_text or customer_tax_scheme_id_text:
            cac_party_tax_scheme = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme')

            if company_id_text:
                cbc_company_id = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
                cbc_company_id.text = company_id_text

            if customer_tax_scheme_id_text:
                cac_tax_scheme = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                cbc_id = ET.SubElement(cac_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                cbc_id.text = customer_tax_scheme_id_text

        if registration_name_text or legal_entity_company_id_text:
            cac_party_legal_entity = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')

            if registration_name_text:
                cbc_registration_name = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
                cbc_registration_name.text = registration_name_text

            if legal_entity_company_id_text and legal_entity_company_shcemeid_text:
                cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID', schemeID=legal_entity_company_shcemeid_text)
                cbc_company_id.text = legal_entity_company_id_text
            elif legal_entity_company_id_text and legal_entity_company_shcemeid_text:
                cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
                cbc_company_id.text = legal_entity_company_id_text

        if contact_name_text or contact_telephone_text or contact_email_text:
            cac_contact = ET.SubElement(cac_cus_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Contact')

            if contact_name_text:
                cbc_name = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
                cbc_name.text = contact_name_text

            if contact_telephone_text:
                cbc_telephone = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Telephone')
                cbc_telephone.text = contact_telephone_text

            if contact_email_text:
                cbc_electronic_mail = ET.SubElement(cac_contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ElectronicMail')
                cbc_electronic_mail.text = contact_email_text


    ##Payeeparty
    payee_id_text = get_text_from_element(root, './PayeeParty/PartyIdentification/ID/IdentifierContent')
    payee_name_text = get_text_from_element(root, './PayeeParty/PartyName/Name/TextContent')
    payee_company_id_text = get_text_from_element(root, './PayeeParty/PartyLegalEntity/CompanyID/IdentifierContent')
    payee_company_shcemeid_text = get_text_from_element(root, './PayeeParty/PartyLegalEntity/CompanyID/schemeID')

    if payee_name_text or payee_id_text or payee_company_id_text:
        cac_payee_party = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PayeeParty')
        
        if payee_id_text:
            cac_party_identification = ET.SubElement(cac_payee_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification')
            cbc_id = ET.SubElement(cac_party_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            cbc_id.text = payee_id_text

        if payee_name_text:
            cac_party_name = ET.SubElement(cac_payee_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
            cbc_name = ET.SubElement(cac_party_name, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
            cbc_name.text = payee_name_text
        

        if payee_company_id_text and payee_company_shcemeid_text:
            cac_party_legal_entity = ET.SubElement(cac_payee_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')
            cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID', schemeID=payee_company_shcemeid_text)
            cbc_company_id.text = payee_company_id_text
        elif payee_company_id_text:
            cac_party_legal_entity = ET.SubElement(cac_payee_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')
            cbc_company_id = ET.SubElement(cac_party_legal_entity, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
            cbc_company_id.text = payee_company_id_text


    #### TaxRepresentativeParty
    party_name_text = get_text_from_element(root, './TaxRepresentativeParty/PartyName/Name/TextContent')
    street_name_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/StreetName/TextContent')
    additional_street_name_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/AdditionalStreetName/TextContent')
    city_name_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/CityName/TextContent')
    postal_zone_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/PostalZone/TextContent')
    country_subentity_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/CountrySubentity/TextContent')
    address_line_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/AddressLine/Line/TextContent')
    country_code_text = get_text_from_element(root, './TaxRepresentativeParty/PostalAddress/Country/IdentificationCode/IdentifierContent')
    company_id_text = get_text_from_element(root, './TaxRepresentativeParty/PartyTaxScheme/CompanyID/IdentifierContent')
    tax_scheme_id_text = get_text_from_element(root, './TaxRepresentativeParty/PartyTaxScheme/TaxScheme/ID/IdentifierContent')

    if (party_name_text or street_name_text or additional_street_name_text or city_name_text or 
        postal_zone_text or country_subentity_text or address_line_text or country_code_text or 
        company_id_text or tax_scheme_id_text):
        
        cac_tax_representative_party = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxRepresentativeParty')
        
        if party_name_text:
            cac_party_name = ET.SubElement(cac_tax_representative_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
            cbc_name = ET.SubElement(cac_party_name, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
            cbc_name.text = party_name_text

        if street_name_text or additional_street_name_text or city_name_text or postal_zone_text or country_subentity_text or address_line_text or country_code_text:
            cac_postal_address = ET.SubElement(cac_tax_representative_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PostalAddress')

            if street_name_text:
                cbc_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StreetName')
                cbc_street_name.text = street_name_text

            if additional_street_name_text:
                cbc_additional_street_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AdditionalStreetName')
                cbc_additional_street_name.text = additional_street_name_text

            if city_name_text:
                cbc_city_name = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName')
                cbc_city_name.text = city_name_text

            if postal_zone_text:
                cbc_postal_zone = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PostalZone')
                cbc_postal_zone.text = postal_zone_text

            if country_subentity_text:
                cbc_country_subentity = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CountrySubentity')
                cbc_country_subentity.text = country_subentity_text

            if address_line_text:
                cac_address_line = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AddressLine')
                cbc_line = ET.SubElement(cac_address_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Line')
                cbc_line.text = address_line_text

            if country_code_text:
                cac_country = ET.SubElement(cac_postal_address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country')
                cbc_identification_code = ET.SubElement(cac_country, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
                cbc_identification_code.text = "AU"

        if company_id_text or tax_scheme_id_text:
            cac_party_tax_scheme = ET.SubElement(cac_tax_representative_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyTaxScheme')

            if company_id_text:
                cbc_company_id = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID')
                cbc_company_id.text = company_id_text

            if tax_scheme_id_text:
                cac_tax_scheme = ET.SubElement(cac_party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                cbc_id = ET.SubElement(cac_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                cbc_id.text = tax_scheme_id_text

    ##Delivery
    actual_delivery_date_text = get_text_from_element(root, './/ActualDeliveryDate/DateContent')
    delivery_location_id_text = get_text_from_element(root, './/DeliveryLocation/ID/IdentifierContent')
    delivery_location_schemeid_text = get_text_from_element(root, './/DeliveryLocation/ID/schemeID')
    
    delivery_location_street_name_text = get_text_from_element(root, './/DeliveryLocation/Address/StreetName/TextContent')
    delivery_location_additional_street_name_text = get_text_from_element(root, './/DeliveryLocation/Address/AdditionalStreetName/TextContent')
    delivery_location_city_name_text = get_text_from_element(root, './/DeliveryLocation/Address/CityName/TextContent')
    delivery_location_postal_zone_text = get_text_from_element(root, './/DeliveryLocation/Address/PostalZone/TextContent')
    delivery_location_country_subentity_text = get_text_from_element(root, './/DeliveryLocation/Address/CountrySubentity/TextContent')
    delivery_location_address_line_text = get_text_from_element(root, './/DeliveryLocation/Address/AddressLine/Line/TextContent')
    delivery_location_country_code_text = get_text_from_element(root, './/DeliveryLocation/Address/Country/IdentificationCode/IdentifierContent')
    delivery_party_name_text = get_text_from_element(root, './/DeliveryParty/PartyName/Name/TextContent')

    if (actual_delivery_date_text or delivery_location_id_text or delivery_location_street_name_text or delivery_location_additional_street_name_text or 
        delivery_location_city_name_text or delivery_location_postal_zone_text or delivery_location_country_subentity_text or delivery_location_address_line_text or 
        delivery_location_country_code_text or delivery_party_name_text):
        
        delivery = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Delivery')

        if actual_delivery_date_text:
            actual_delivery_date = ET.SubElement(delivery, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ActualDeliveryDate')
            actual_delivery_date.text = actual_delivery_date_text

        if (delivery_location_id_text or delivery_location_street_name_text or delivery_location_additional_street_name_text or 
            delivery_location_city_name_text or delivery_location_postal_zone_text or delivery_location_country_subentity_text or 
            delivery_location_address_line_text or delivery_location_country_code_text):
            
            delivery_location = ET.SubElement(delivery, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}DeliveryLocation')
            
            if delivery_location_id_text and delivery_location_schemeid_text:
                delivery_location_id = ET.SubElement(delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', schemeID=delivery_location_schemeid_text)
                delivery_location_id.text = delivery_location_id_text
            elif delivery_location_id_text:
                delivery_location_id = ET.SubElement(delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                delivery_location_id.text = delivery_location_id_text

            ADD_delivery_location = ET.SubElement(delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Address')

            if delivery_location_street_name_text:
                street_name = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StreetName')
                street_name.text = delivery_location_street_name_text

            if delivery_location_additional_street_name_text:
                additional_street_name = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AdditionalStreetName')
                additional_street_name.text = delivery_location_additional_street_name_text

            if delivery_location_city_name_text:
                city_name = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName')
                city_name.text = delivery_location_city_name_text

            if delivery_location_postal_zone_text:
                postal_zone = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PostalZone')
                postal_zone.text = delivery_location_postal_zone_text

            if delivery_location_country_subentity_text:
                country_subentity = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CountrySubentity')
                country_subentity.text = delivery_location_country_subentity_text

            if delivery_location_address_line_text:
                address_line = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AddressLine')
                line = ET.SubElement(address_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Line')
                line.text = delivery_location_address_line_text

            if delivery_location_country_code_text:
                country = ET.SubElement(ADD_delivery_location, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country')
                identification_code = ET.SubElement(country, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
                identification_code.text = delivery_location_country_code_text

        if delivery_party_name_text:
            delivery_party = ET.SubElement(delivery, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}DeliveryParty')
            party_name = ET.SubElement(delivery_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyName')
            name = ET.SubElement(party_name, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
            name.text = delivery_party_name_text


    #PaymentMeans
    payment_means_code_text = get_text_from_element(root, './/PaymentMeansCode/IdentifierContent')
    payment_means_namecode_text = get_text_from_element(root, './/PaymentMeansCode/name')
    payment_id_text = get_text_from_element(root, './/PaymentID/TextContent')
    account_id_text = get_text_from_element(root, './/PayeeFinancialAccount/ID/IdentifierContent')
    account_name_text = get_text_from_element(root, './/PayeeFinancialAccount/Name/TextContent')
    branch_id_text = get_text_from_element(root, './/PayeeFinancialAccount/FinancialInstitutionBranch/ID/IdentifierContent')

    if payment_means_code_text or payment_id_text or account_id_text or account_name_text or branch_id_text:
        
        cac_payment_means = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PaymentMeans')

        if payment_means_code_text and payment_means_namecode_text:
            cbc_payment_means_code = ET.SubElement(cac_payment_means, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentMeansCode', name=payment_means_namecode_text)
            cbc_payment_means_code.text = payment_means_code_text
        elif payment_means_code_text:
            cbc_payment_means_code = ET.SubElement(cac_payment_means, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentMeansCode')
            cbc_payment_means_code.text = payment_means_code_text
        
        if payment_id_text:
            cbc_payment_id = ET.SubElement(cac_payment_means, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PaymentID')
            cbc_payment_id.text = payment_id_text

        if account_id_text or account_name_text or branch_id_text:
            cac_payee_financial_account = ET.SubElement(cac_payment_means, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PayeeFinancialAccount')

            if account_id_text:
                cbc_account_id = ET.SubElement(cac_payee_financial_account, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                cbc_account_id.text = account_id_text

            if account_name_text:
                cbc_account_name = ET.SubElement(cac_payee_financial_account, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
                cbc_account_name.text = account_name_text

            if branch_id_text:
                cac_financial_institution_branch = ET.SubElement(cac_payee_financial_account, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}FinancialInstitutionBranch')
                cbc_branch_id = ET.SubElement(cac_financial_institution_branch, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                cbc_branch_id.text = branch_id_text


    ###PaymentTerms
    payment_terms_note_text = get_text_from_element(root, './/PaymentTerms/Note/TextContent')

    if payment_terms_note_text:
        payment_terms = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PaymentTerms')

        if payment_terms_note_text:
            note = ET.SubElement(payment_terms, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Note')
            note.text = payment_terms_note_text


    ###AllowanceCharge
    charge_indicator_text = get_text_from_element(root, './/ChargeIndicator/IdentifierContent')
    allowance_charge_reason_code_text = get_text_from_element(root, './/AllowanceChargeReasonCode/IdentifierContent')
    allowance_charge_reason_text = get_text_from_element(root, './/AllowanceChargeReason/TextContent')
    multiplier_factor_numeric_text = get_text_from_element(root, './/MultiplierFactorNumeric/NumericContent')
    amount_text = get_text_from_element(root, './/Amount/AmountContent')
    base_amount_text = get_text_from_element(root, './/BaseAmount/AmountContent')
    tax_category_id_text = get_text_from_element(root, './/TaxCategory/ID/IdentifierContent')
    tax_category_percent_text = get_text_from_element(root, './/TaxCategory/Percent/NumericContent')
    allow_tax_scheme_id_text = get_text_from_element(root, './/TaxCategory/TaxScheme/ID/IdentifierContent')

    if (charge_indicator_text or allowance_charge_reason_code_text or allowance_charge_reason_text or multiplier_factor_numeric_text or amount_text or 
        base_amount_text or tax_category_id_text or tax_category_percent_text or allow_tax_scheme_id_text):
        
        allowance_charge = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AllowanceCharge')

        if charge_indicator_text:
            charge_indicator = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ChargeIndicator')
            charge_indicator.text = charge_indicator_text

        if allowance_charge_reason_code_text:
            allowance_charge_reason_code = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AllowanceChargeReasonCode')
            allowance_charge_reason_code.text = allowance_charge_reason_code_text
        
        if allowance_charge_reason_text:
            allowance_charge_reason_code = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AllowanceChargeReason')
            allowance_charge_reason_code.text = allowance_charge_reason_text

        if multiplier_factor_numeric_text:
            multiplier_factor_numeric = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}MultiplierFactorNumeric')
            multiplier_factor_numeric.text = multiplier_factor_numeric_text

        if amount_text:
            amount = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Amount', currencyID="AUD")
            amount.text = amount_text

        if base_amount_text:
            base_amount = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}BaseAmount', currencyID="AUD")
            base_amount.text = base_amount_text

        if tax_category_id_text or tax_category_percent_text or allow_tax_scheme_id_text:
            tax_category = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxCategory')

            if tax_category_id_text:
                tax_category_id = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                tax_category_id.text = tax_category_id_text

            if tax_category_percent_text:
                tax_category_percent = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Percent')
                tax_category_percent.text = tax_category_percent_text

            if allow_tax_scheme_id_text:
                tax_scheme = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                tax_scheme_id = ET.SubElement(tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                tax_scheme_id.text = allow_tax_scheme_id_text


    ####TaxTotal
    tax_amount_text = get_text_from_element(root, './/TaxAmount/AmountContent')
    taxable_amount_text = get_text_from_element(root, './/TaxSubtotal/TaxableAmount/AmountContent')
    subtotal_tax_amount_text = get_text_from_element(root, './/TaxSubtotal/TaxAmount/AmountContent')
    tax_category_id_text = get_text_from_element(root, './/TaxSubtotal/TaxCategory/ID/IdentifierContent')
    tax_category_percent_text = get_text_from_element(root, './/TaxSubtotal/TaxCategory/Percent/NumericContent')
    total_tax_scheme_id_text = get_text_from_element(root, './/TaxSubtotal/TaxCategory/TaxScheme/ID/IdentifierContent')

    if (tax_amount_text or taxable_amount_text or subtotal_tax_amount_text or 
        tax_category_id_text or tax_category_percent_text or total_tax_scheme_id_text):
        
        tax_total = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal')

        if tax_amount_text:
            tax_amount = ET.SubElement(tax_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxAmount', currencyID="AUD")
            tax_amount.text = tax_amount_text

        if (taxable_amount_text or subtotal_tax_amount_text or 
            tax_category_id_text or tax_category_percent_text or total_tax_scheme_id_text):
            
            tax_subtotal = ET.SubElement(tax_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxSubtotal')

            if taxable_amount_text:
                taxable_amount = ET.SubElement(tax_subtotal, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxableAmount', currencyID="AUD")
                taxable_amount.text = taxable_amount_text

            if subtotal_tax_amount_text:
                tax_amount = ET.SubElement(tax_subtotal, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxAmount', currencyID="AUD")
                tax_amount.text = subtotal_tax_amount_text

            if tax_category_id_text or tax_category_percent_text or total_tax_scheme_id_text:
                tax_category = ET.SubElement(tax_subtotal, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxCategory')

                if tax_category_id_text:
                    tax_category_id = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    tax_category_id.text = tax_category_id_text

                if tax_category_percent_text:
                    tax_category_percent = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Percent')
                    tax_category_percent.text = tax_category_percent_text

                if total_tax_scheme_id_text:
                    tax_scheme = ET.SubElement(tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                    tax_scheme_id = ET.SubElement(tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    tax_scheme_id.text = total_tax_scheme_id_text


    # LegalMonetaryTotal
    line_extension_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/LineExtensionAmount/AmountContent')
    tax_exclusive_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/TaxExclusiveAmount/AmountContent')
    tax_inclusive_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/TaxInclusiveAmount/AmountContent')
    charge_total_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/ChargeTotalAmount/AmountContent')
    prepaid_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/PrepaidAmount/AmountContent')
    payable_rounding_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/PayableRoundingAmount/AmountContent')
    payable_amount_text = get_text_from_element(root, './/LegalMonetaryTotal/PayableAmount/AmountContent')

    if (line_extension_amount_text or tax_exclusive_amount_text or tax_inclusive_amount_text or charge_total_amount_text or 
        prepaid_amount_text or payable_rounding_amount_text or payable_amount_text):
        
        legal_monetary_total = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}LegalMonetaryTotal')

        if line_extension_amount_text:
            line_extension_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineExtensionAmount', currencyID="AUD")
            line_extension_amount.text = line_extension_amount_text

        if tax_exclusive_amount_text:
            tax_exclusive_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxExclusiveAmount', currencyID="AUD")
            tax_exclusive_amount.text = tax_exclusive_amount_text

        if tax_inclusive_amount_text:
            tax_inclusive_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxInclusiveAmount', currencyID="AUD")
            tax_inclusive_amount.text = tax_inclusive_amount_text

        if charge_total_amount_text:
            charge_total_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ChargeTotalAmount', currencyID="AUD")
            charge_total_amount.text = charge_total_amount_text

        if prepaid_amount_text:
            prepaid_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PrepaidAmount', currencyID="AUD")
            prepaid_amount.text = prepaid_amount_text

        if payable_rounding_amount_text:
            payable_rounding_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PayableRoundingAmount')
            payable_rounding_amount.text = payable_rounding_amount_text

        if payable_amount_text:
            payable_amount = ET.SubElement(legal_monetary_total, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PayableAmount', currencyID="AUD")
            payable_amount.text = payable_amount_text


    # InvoiceLine
    invoice_lines = root.findall('.//InvoiceLine')
    for invoice_line in invoice_lines:
        ubl_invoice_line = ET.SubElement(ubl_root, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoiceLine')
 
        id_text = get_text_from_element(invoice_line, './ID/IdentifierContent')
        note_text = get_text_from_element(invoice_line, './Note/TextContent')
        invoiced_quantity_text = get_text_from_element(invoice_line, './InvoicedQuantity/NumericContent')
        invoiced_quantity_unitCode_text = get_text_from_element(invoice_line, './InvoicedQuantity/unitCode')
        
        line_extension_amount_text = get_text_from_element(invoice_line, './LineExtensionAmount/AmountContent')
        accounting_cost_text = get_text_from_element(invoice_line, './AccountingCost/TextContent')
        invoice_period_start_date_text = get_text_from_element(invoice_line, './/InvoicePeriod/StartDate/DateContent')
        invoice_period_end_date_text = get_text_from_element(invoice_line, './/InvoicePeriod/EndDate/DateContent')
        order_line_reference_id_text = get_text_from_element(invoice_line, './/OrderLineReference/LineID/IdentifierContent')
        document_reference_id_text = get_text_from_element(invoice_line, './/DocumentReference/ID/IdentifierContent')
        document_reference_schemeID_text = get_text_from_element(invoice_line, './/DocumentReference/ID/schemeID')
        
        document_reference_document_type_code_text = get_text_from_element(invoice_line, './/DocumentReference/DocumentTypeCode/IdentifierContent')
        item_description_text = get_text_from_element(invoice_line, './/Item/Description/TextContent')
        item_name_text = get_text_from_element(invoice_line, './/Item/Name/TextContent')
        buyers_item_identification_id_text = get_text_from_element(invoice_line, './/Item/BuyersItemIdentification/ID/IdentifierContent')
        sellers_item_identification_id_text = get_text_from_element(invoice_line, './/Item/SellersItemIdentification/ID/IdentifierContent')
        standard_item_identification_id_text = get_text_from_element(invoice_line, './/Item/StandardItemIdentification/ID/IdentifierContent')
        standard_item_identification_schemeID_text = get_text_from_element(invoice_line, './/Item/StandardItemIdentification/ID/schemeID')
        
        origin_country_identification_code_text = get_text_from_element(invoice_line, './/Item/OriginCountry/IdentificationCode/IdentifierContent')
        item_classification_code_text = get_text_from_element(invoice_line, './/Item/CommodityClassification/ItemClassificationCode/IdentifierContent')
        item_classification_listID_text = get_text_from_element(invoice_line, './/Item/CommodityClassification/ItemClassificationCode/listID')
        
        classified_tax_category_id_text = get_text_from_element(invoice_line, './/Item/ClassifiedTaxCategory/ID/IdentifierContent')
        classified_tax_category_percent_text = get_text_from_element(invoice_line, './/Item/ClassifiedTaxCategory/Percent/NumericContent')
        classified_tax_category_tax_scheme_id_text = get_text_from_element(invoice_line, './/Item/ClassifiedTaxCategory/TaxScheme/ID/IdentifierContent')
        price_amount_text = get_text_from_element(invoice_line, './/Price/PriceAmount/AmountContent')
        base_quantity_text = get_text_from_element(invoice_line, './/Price/BaseQuantity/AmountContent')
        charge_indicator_text = get_text_from_element(invoice_line, './/Price/AllowanceCharge/ChargeIndicator/IdentifierContent')
        allowance_charge_amount_text = get_text_from_element(invoice_line, './/Price/AllowanceCharge/Amount/AmountContent')
        allowance_charge_base_amount_text = get_text_from_element(invoice_line, './/Price/AllowanceCharge/BaseAmount/AmountContent')

    
        if (id_text or note_text or invoiced_quantity_text or line_extension_amount_text or accounting_cost_text or 
        invoice_period_start_date_text or invoice_period_end_date_text or order_line_reference_id_text or 
        document_reference_id_text or document_reference_document_type_code_text or item_description_text or 
        item_name_text or buyers_item_identification_id_text or sellers_item_identification_id_text or 
        standard_item_identification_id_text or origin_country_identification_code_text or 
        item_classification_code_text or classified_tax_category_id_text or classified_tax_category_percent_text or 
        classified_tax_category_tax_scheme_id_text or price_amount_text or base_quantity_text or 
        charge_indicator_text or allowance_charge_amount_text or allowance_charge_base_amount_text):
        
            if id_text:
                id_element = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                id_element.text = id_text

            if note_text:
                note = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Note')
                note.text = note_text

            if invoiced_quantity_text and invoiced_quantity_unitCode_text:
                invoiced_quantity = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoicedQuantity', unitCode=invoiced_quantity_unitCode_text)
                invoiced_quantity.text = invoiced_quantity_text
            elif invoiced_quantity_text:
                invoiced_quantity = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoicedQuantity')
                invoiced_quantity.text = invoiced_quantity_text

            if line_extension_amount_text:
                line_extension_amount = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineExtensionAmount', currencyID="AUD")
                line_extension_amount.text = line_extension_amount_text

            if accounting_cost_text:
                accounting_cost = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}AccountingCost')
                accounting_cost.text = accounting_cost_text

            if invoice_period_start_date_text or invoice_period_end_date_text:
                invoice_period = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoicePeriod')

                if invoice_period_start_date_text:
                    start_date = ET.SubElement(invoice_period, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}StartDate')
                    start_date.text = invoice_period_start_date_text

                if invoice_period_end_date_text:
                    end_date = ET.SubElement(invoice_period, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}EndDate')
                    end_date.text = invoice_period_end_date_text

            if order_line_reference_id_text:
                order_line_reference = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}OrderLineReference')
                line_id = ET.SubElement(order_line_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineID')
                line_id.text = order_line_reference_id_text

            if document_reference_id_text or document_reference_document_type_code_text:
                document_reference = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}DocumentReference')

                if document_reference_id_text and document_reference_schemeID_text:
                    doc_id = ET.SubElement(document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', schemeID=document_reference_schemeID_text)
                    doc_id.text = document_reference_id_text
                elif document_reference_id_text:
                    doc_id = ET.SubElement(document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    doc_id.text = document_reference_id_text

                if document_reference_document_type_code_text:
                    document_type_code = ET.SubElement(document_reference, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DocumentTypeCode')
                    document_type_code.text = document_reference_document_type_code_text

            if (item_description_text or item_name_text or buyers_item_identification_id_text or 
            sellers_item_identification_id_text or standard_item_identification_id_text or 
            origin_country_identification_code_text or item_classification_code_text or 
            classified_tax_category_id_text or classified_tax_category_percent_text or 
            classified_tax_category_tax_scheme_id_text):
                
                item = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Item')

                if item_description_text:
                    description = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Description')
                    description.text = item_description_text

                if item_name_text:
                    name = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
                    name.text = item_name_text

                if buyers_item_identification_id_text:
                    buyers_item_identification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}BuyersItemIdentification')
                    buyer_id = ET.SubElement(buyers_item_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    buyer_id.text = buyers_item_identification_id_text

                if sellers_item_identification_id_text:
                    sellers_item_identification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}SellersItemIdentification')
                    seller_id = ET.SubElement(sellers_item_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    seller_id.text = sellers_item_identification_id_text

                if standard_item_identification_id_text:
                    standard_item_identification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}StandardItemIdentification')
                    standard_id = ET.SubElement(standard_item_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID', schemeID=standard_item_identification_schemeID_text)
                    standard_id.text = standard_item_identification_id_text
                elif standard_item_identification_id_text:
                    standard_item_identification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}StandardItemIdentification')
                    standard_id = ET.SubElement(standard_item_identification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                    standard_id.text = standard_item_identification_id_text

                if origin_country_identification_code_text:
                    origin_country = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}OriginCountry')
                    identification_code = ET.SubElement(origin_country, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode')
                    identification_code.text = origin_country_identification_code_text

                if item_classification_code_text and item_classification_listID_text:
                    commodity_classification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}CommodityClassification')
                    item_classification_code = ET.SubElement(commodity_classification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ItemClassificationCode', listID=item_classification_listID_text)
                    item_classification_code.text = item_classification_code_text
                elif item_classification_code_text:
                    commodity_classification = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}CommodityClassification')
                    item_classification_code = ET.SubElement(commodity_classification, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ItemClassificationCode')
                    item_classification_code.text = item_classification_code_text

                if (classified_tax_category_id_text or classified_tax_category_percent_text or 
                classified_tax_category_tax_scheme_id_text):
                    classified_tax_category = ET.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}ClassifiedTaxCategory')

                    if classified_tax_category_id_text:
                        classified_tax_category_id = ET.SubElement(classified_tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                        classified_tax_category_id.text = classified_tax_category_id_text

                    if classified_tax_category_percent_text:
                        classified_tax_category_percent = ET.SubElement(classified_tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Percent')
                        classified_tax_category_percent.text = classified_tax_category_percent_text

                    if classified_tax_category_tax_scheme_id_text:
                        classified_tax_category_tax_scheme = ET.SubElement(classified_tax_category, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme')
                        tax_scheme_id = ET.SubElement(classified_tax_category_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
                        tax_scheme_id.text = classified_tax_category_tax_scheme_id_text

            if (price_amount_text or base_quantity_text or charge_indicator_text or 
            allowance_charge_amount_text or allowance_charge_base_amount_text):
                price = ET.SubElement(ubl_invoice_line, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Price')

                if price_amount_text:
                    price_amount = ET.SubElement(price, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}PriceAmount', currencyID="AUD")
                    price_amount.text = price_amount_text

                if base_quantity_text:
                    base_quantity = ET.SubElement(price, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}BaseQuantity')
                    base_quantity.text = base_quantity_text

                if charge_indicator_text or allowance_charge_amount_text or allowance_charge_base_amount_text:
                    allowance_charge = ET.SubElement(price, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AllowanceCharge')

                    if charge_indicator_text:
                        charge_indicator = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ChargeIndicator')
                        charge_indicator.text = charge_indicator_text

                    if allowance_charge_amount_text:
                        amount = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Amount', currencyID="AUD")
                        amount.text = allowance_charge_amount_text

                    if allowance_charge_base_amount_text:
                        base_amount = ET.SubElement(allowance_charge, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}BaseAmount', currencyID="AUD")
                        base_amount.text = allowance_charge_base_amount_text

    # Write to the output file
    tree = ET.ElementTree(ubl_root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)


# Transform json to xml
def transform_to_xml(json_data):
    root = ET.Element("Invoice")

    def handle_dict_to_xml(parent, key, value):
        if isinstance(value, list):
            for item in value:
                sub_elem = ET.SubElement(parent, key)
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        handle_dict_to_xml(sub_elem, sub_key, sub_value)
                else:
                    if item is not None:  # Check if the item is not empty
                        sub_elem.text = str(item)
        else:
            sub_elem = ET.SubElement(parent, key)
            if value is not None:  # Check if the value is not empty
                sub_elem.text = str(value)

    for key, val in json_data.items():
        if key.startswith("_"):
            continue
        if val is not None:  # Check if the value is not empty
            for item in val:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        handle_dict_to_xml(root, sub_key, sub_value)
                else:
                    if item is not None:  # Check if the item is not empty
                        handle_dict_to_xml(root, key, item)

    return root