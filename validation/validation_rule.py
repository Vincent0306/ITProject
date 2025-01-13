import xml.etree.ElementTree as ET
from datetime import datetime


# Function to get the text content of an XML element
def get_text_from_element(element):
    return element.text if element is not None else None

## validate initial xml
def check_type(value, expected_type):
    try:
        if expected_type == float:
            float(value)
        elif expected_type == int:
            int(value)
        elif expected_type == str:
            return isinstance(value, str)
        elif expected_type == 'date':
            # parse date as %Y-%m-%d
            datetime.strptime(value, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

# Validate initial XML
def validate_input(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    validation_result = {}
    details = {}

    required_elements = {
        'ID': ('.//ID/IdentifierContent', str),
        'IssueDate(Y-M-D)': ('.//IssueDate/DateContent', 'date'),
        'DueDate(Y-M-D)': ('.//DueDate/DateContent', 'date'),
        'InvoiceTypeCode': ('.//InvoiceTypeCode/IdentifierContent', str),
        'Note': ('.//Note/TextContent', str),
        'DocumentCurrencyCode': ('.//DocumentCurrencyCode/IdentifierContent', str),
        'AccountingCost': ('.//AccountingCost/TextContent', str),
        'BuyerReference': ('.//BuyerReference/TextContent', str),
        'InvoicePeriodStartDate(Y-M-D)': ('.//InvoicePeriod/StartDate/DateContent', 'date'),
        'InvoicePeriodEndDate(Y-M-D)': ('.//InvoicePeriod/EndDate/DateContent', 'date'),
        'OrderReferenceID': ('.//OrderReference/ID/IdentifierContent', str),
        'OrderReferenceSalesOrderID': ('.//OrderReference/SalesOrderID/IdentifierContent', str),
        'BillingReferenceInvoiceDocumentReferenceID': ('.//BillingReference/InvoiceDocumentReference/ID/IdentifierContent', str),
        'BillingReferenceInvoiceDocumentReferenceIssueDate': ('.//BillingReference/InvoiceDocumentReference/IssueDate/DateContent', 'date'),
        'DespatchDocumentReferenceID': ('.//DespatchDocumentReference/ID/IdentifierContent', str),
        'ReceiptDocumentReferenceID': ('.//ReceiptDocumentReference/ID/IdentifierContent', str),
        'OriginatorDocumentReferenceID': ('.//OriginatorDocumentReference/ID/IdentifierContent', str),
        'ContractDocumentReferenceID': ('.//ContractDocumentReference/ID/IdentifierContent', str),
        'SupplierEndpointID': ('.//AccountingSupplierParty/Party/EndpointID/IdentifierContent', str),
        'SupplierPartyIdentificationID': ('.//AccountingSupplierParty/Party/PartyIdentification/ID/IdentifierContent', str),
        'SupplierPartyName': ('.//AccountingSupplierParty/Party/PartyName/Name/TextContent', str),
        'SupplierStreetName': ('.//AccountingSupplierParty/Party/PostalAddress/StreetName/TextContent', str),
        'SupplierAdditionalStreetName': ('.//AccountingSupplierParty/Party/PostalAddress/AdditionalStreetName/TextContent', str),
        'SupplierCityName': ('.//AccountingSupplierParty/Party/PostalAddress/CityName/TextContent', str),
        'SupplierPostalZone': ('.//AccountingSupplierParty/Party/PostalAddress/PostalZone/TextContent', str),
        'SupplierCountryIdentificationCode': ('.//AccountingSupplierParty/Party/PostalAddress/Country/IdentificationCode/IdentifierContent', str),
        'SupplierCompanyID': ('.//AccountingSupplierParty/Party/PartyTaxScheme/CompanyID/IdentifierContent', str),
        'SupplierTaxSchemeID': ('.//AccountingSupplierParty/Party/PartyTaxScheme/TaxScheme/ID/IdentifierContent', str),
        'SupplierRegistrationName': ('.//AccountingSupplierParty/Party/PartyLegalEntity/RegistrationName/TextContent', str),
        'SupplierCompanyID': ('.//AccountingSupplierParty/Party/PartyLegalEntity/CompanyID/IdentifierContent', str),
        'SupplierCompanyLegalForm': ('.//AccountingSupplierParty/Party/PartyLegalEntity/CompanyLegalForm/TextContent', str),
        'SupplierContactName': ('.//AccountingSupplierParty/Party/Contact/Name/TextContent', str),
        'SupplierContactTelephone': ('.//AccountingSupplierParty/Party/Contact/Telephone/TextContent', str),
        'SupplierContactEmail': ('.//AccountingSupplierParty/Party/Contact/ElectronicMail/TextContent', str),
        'CustomerEndpointID': ('.//AccountingCustomerParty/Party/EndpointID/IdentifierContent', str),
        'CustomerPartyIdentificationID': ('.//AccountingCustomerParty/Party/PartyIdentification/ID/IdentifierContent', str),
        'CustomerPartyName': ('.//AccountingCustomerParty/Party/PartyName/Name/TextContent', str),
        'CustomerStreetName': ('.//AccountingCustomerParty/Party/PostalAddress/StreetName/TextContent', str),
        'CustomerAdditionalStreetName': ('.//AccountingCustomerParty/Party/PostalAddress/AdditionalStreetName/TextContent', str),
        'CustomerCityName': ('.//AccountingCustomerParty/Party/PostalAddress/CityName/TextContent', str),
        'CustomerPostalZone': ('.//AccountingCustomerParty/Party/PostalAddress/PostalZone/TextContent', str),
        'CustomerCountryIdentificationCode': ('.//AccountingCustomerParty/Party/PostalAddress/Country/IdentificationCode/IdentifierContent', str),
        'CustomerTaxCompanyID': ('.//AccountingCustomerParty/Party/PartyTaxScheme/CompanyID/IdentifierContent', str),
        'CustomerTaxSchemeID': ('.//AccountingCustomerParty/Party/PartyTaxScheme/TaxScheme/ID/IdentifierContent', str),
        'CustomerRegistrationName': ('.//AccountingCustomerParty/Party/PartyLegalEntity/RegistrationName/TextContent', str),
        'CustomerCompanyID': ('.//AccountingCustomerParty/Party/PartyLegalEntity/CompanyID/IdentifierContent', str),
        'CustomerContactName': ('.//AccountingCustomerParty/Party/Contact/Name/TextContent', str),
        'CustomerContactTelephone': ('.//AccountingCustomerParty/Party/Contact/Telephone/TextContent', str),
        'CustomerContactEmail': ('.//AccountingCustomerParty/Party/Contact/ElectronicMail/TextContent', str),
        'PayeePartyIdentificationID': ('.//PayeeParty/PartyIdentification/ID/IdentifierContent', str),
        'PayeePartyName': ('.//PayeeParty/PartyName/Name/TextContent', str),
        'PayeePartyCompanyID': ('.//PayeeParty/PartyLegalEntity/CompanyID/IdentifierContent', str),
        'TaxRepresentativePartyName': ('.//TaxRepresentativeParty/PartyName/Name/TextContent', str),
        'TaxRepresentativeStreetName': ('.//TaxRepresentativeParty/PostalAddress/StreetName/TextContent', str),
        'TaxRepresentativeAdditionalStreetName': ('.//TaxRepresentativeParty/PostalAddress/AdditionalStreetName/TextContent', str),
        'TaxRepresentativeCityName': ('.//TaxRepresentativeParty/PostalAddress/CityName/TextContent', str),
        'TaxRepresentativePostalZone': ('.//TaxRepresentativeParty/PostalAddress/PostalZone/TextContent', str),
        'TaxRepresentativeCountrySubentity': ('.//TaxRepresentativeParty/PostalAddress/CountrySubentity/TextContent', str),
        'TaxRepresentativeAddressLine': ('.//TaxRepresentativeParty/PostalAddress/AddressLine/Line/TextContent', str),
        'TaxRepresentativeCountryIdentificationCode': ('.//TaxRepresentativeParty/PostalAddress/Country/IdentificationCode/IdentifierContent', str),
        'TaxRepresentativeCompanyID': ('.//TaxRepresentativeParty/PartyTaxScheme/CompanyID/IdentifierContent', str),
        'TaxRepresentativeTaxSchemeID': ('.//TaxRepresentativeParty/PartyTaxScheme/TaxScheme/ID/IdentifierContent', str),
        'DeliveryActualDeliveryDate(Y-M-D)': ('.//Delivery/ActualDeliveryDate/DateContent', 'date'),
        'DeliveryLocationID': ('.//Delivery/DeliveryLocation/ID/IdentifierContent', str),
        'DeliveryStreetName': ('.//Delivery/DeliveryLocation/Address/StreetName/TextContent', str),
        'DeliveryAdditionalStreetName': ('.//Delivery/DeliveryLocation/Address/AdditionalStreetName/TextContent', str),
        'DeliveryCityName': ('.//Delivery/DeliveryLocation/Address/CityName/TextContent', str),
        'DeliveryPostalZone': ('.//Delivery/DeliveryLocation/Address/PostalZone/TextContent', str),
        'DeliveryCountrySubentity': ('.//Delivery/DeliveryLocation/Address/CountrySubentity/TextContent', str),
        'DeliveryAddressLine': ('.//Delivery/DeliveryLocation/Address/AddressLine/Line/TextContent', str),
        'DeliveryCountryIdentificationCode': ('.//Delivery/DeliveryLocation/Address/Country/IdentificationCode/IdentifierContent', str),
        'DeliveryPartyName': ('.//Delivery/DeliveryParty/PartyName/Name/TextContent', str),
        'PaymentMeansCode': ('.//PaymentMeans/PaymentMeansCode/IdentifierContent', str),
        'PaymentID': ('.//PaymentMeans/PaymentID/TextContent', str),
        'PayeeFinancialAccountID': ('.//PaymentMeans/PayeeFinancialAccount/ID/IdentifierContent', str),
        'PayeeFinancialAccountName': ('.//PaymentMeans/PayeeFinancialAccount/Name/TextContent', str),
        'PayeeFinancialInstitutionBranchID': ('.//PaymentMeans/PayeeFinancialAccount/FinancialInstitutionBranch/ID/IdentifierContent', str),
        'PaymentTermsNote': ('.//PaymentTerms/Note/TextContent', str),
        'ChargeIndicator': ('.//AllowanceCharge/ChargeIndicator/IdentifierContent', str),
        'AllowanceChargeReasonCode': ('.//AllowanceCharge/AllowanceChargeReasonCode/IdentifierContent', str),
        'AllowanceChargeReason': ('.//AllowanceCharge/AllowanceChargeReason/TextContent', str),
        'MultiplierFactorNumeric': ('.//AllowanceCharge/MultiplierFactorNumeric/NumericContent', float),
        'AllowanceChargeAmount': ('.//AllowanceCharge/Amount/AmountContent', float),
        'BaseAmount': ('.//AllowanceCharge/BaseAmount/AmountContent', float),
        'TaxCategoryID': ('.//AllowanceCharge/TaxCategory/ID/IdentifierContent', str),
        'TaxCategoryPercent': ('.//AllowanceCharge/TaxCategory/Percent/NumericContent', float),
        'TaxCategoryTaxSchemeID': ('.//AllowanceCharge/TaxCategory/TaxScheme/ID/IdentifierContent', str),
        'TaxAmount': ('.//TaxTotal/TaxAmount/AmountContent', float),
        'TaxSubtotalTaxableAmount': ('.//TaxTotal/TaxSubtotal/TaxableAmount/AmountContent', float),
        'TaxSubtotalTaxAmount': ('.//TaxTotal/TaxSubtotal/TaxAmount/AmountContent', float),
        'TaxSubtotalTaxCategoryID': ('.//TaxTotal/TaxSubtotal/TaxCategory/ID/IdentifierContent', str),
        'TaxSubtotalTaxCategoryPercent': ('.//TaxTotal/TaxSubtotal/TaxCategory/Percent/NumericContent', float),
        'TaxSubtotalTaxSchemeID': ('.//TaxTotal/TaxSubtotal/TaxCategory/TaxScheme/ID/IdentifierContent', str),
        'LineExtensionAmount': ('.//LegalMonetaryTotal/LineExtensionAmount/AmountContent', float),
        'TaxExclusiveAmount': ('.//LegalMonetaryTotal/TaxExclusiveAmount/AmountContent', float),
        'TaxInclusiveAmount': ('.//LegalMonetaryTotal/TaxInclusiveAmount/AmountContent', float),
        'ChargeTotalAmount': ('.//LegalMonetaryTotal/ChargeTotalAmount/AmountContent', float),
        'PrepaidAmount': ('.//LegalMonetaryTotal/PrepaidAmount/AmountContent', float),
        'PayableAmount': ('.//LegalMonetaryTotal/PayableAmount/AmountContent', float),
    }

    invoice_line_elements = {
        'InvoiceLineID': ('ID/IdentifierContent', str),
        'InvoiceLineNote': ('Note/TextContent', str),
        'InvoiceLineInvoicedQuantity': ('InvoicedQuantity/NumericContent', float),
        'InvoiceLineLineExtensionAmount': ('LineExtensionAmount/AmountContent', float),
        'InvoiceLineAccountingCost': ('AccountingCost/TextContent', str),
        'InvoiceLineStartDate(Y-M-D)': ('InvoicePeriod/StartDate/DateContent', 'date'),
        'InvoiceLineEndDate(Y-M-D)': ('InvoicePeriod/EndDate/DateContent', 'date'),
        'InvoiceLineOrderLineReferenceID': ('OrderLineReference/LineID/IdentifierContent', str),
        'InvoiceLineDocumentReferenceID': ('DocumentReference/ID/IdentifierContent', str),
        'InvoiceLineDocumentReferenceTypeCode': ('DocumentReference/DocumentTypeCode/IdentifierContent', str),
        'InvoiceLineItemDescription': ('Item/Description/TextContent', str),
        'InvoiceLineItemName': ('Item/Name/TextContent', str),
        'InvoiceLineBuyersItemIdentificationID': ('Item/BuyersItemIdentification/ID/IdentifierContent', str),
        'InvoiceLineSellersItemIdentificationID': ('Item/SellersItemIdentification/ID/IdentifierContent', str),
        'InvoiceLineStandardItemIdentificationID': ('Item/StandardItemIdentification/ID/IdentifierContent', str),
        'InvoiceLineOriginCountryIdentificationCode': ('Item/OriginCountry/IdentificationCode/IdentifierContent', str),
        'InvoiceLineCommodityClassificationCode': ('Item/CommodityClassification/ItemClassificationCode/IdentifierContent', str),
        'InvoiceLineTaxCategoryID': ('Item/ClassifiedTaxCategory/ID/IdentifierContent', str),
        'InvoiceLineTaxCategoryPercent': ('Item/ClassifiedTaxCategory/Percent/NumericContent', float),
        'InvoiceLineTaxSchemeID': ('Item/ClassifiedTaxCategory/TaxScheme/ID/IdentifierContent', str),
        'InvoiceLinePriceAmount': ('Price/PriceAmount/AmountContent', float),
        'InvoiceLineAllowanceChargeIndicator': ('Price/AllowanceCharge/ChargeIndicator/IdentifierContent', str),
        'InvoiceLineAllowanceChargeAmount': ('Price/AllowanceCharge/Amount/AmountContent', float),
        'InvoiceLineBaseAmount': ('Price/AllowanceCharge/BaseAmount/AmountContent', float)
    }

    for key, (path, expected_type) in required_elements.items():
        element = root.find(path)
        if element is not None and element.text is not None:
            element_text = element.text.strip()
            if element_text == "Please Enter Customer ID (ABN)" or element_text == "Please Enter your account number for payment" \
            or element_text == "Please Enter your PaymentTerms":
                validation_result[key] = 0
                details[key] = element_text
            elif element_text and check_type(element_text, expected_type):
                validation_result[key] = 1
                details[key] = element_text

            else:
                validation_result[key] = 0
                details[key] = element_text
        # Skip elements that are not found in the XML file
        else:
            continue
    
    # Validate multiple InvoiceLine elements
    invoice_lines = root.findall('.//InvoiceLine')

    for index, invoice_line in enumerate(invoice_lines):
        line_key = f"InvoiceLine_{index + 1}"
        validation_result[line_key] = {}
        details[line_key] = {}
        for key, (relative_path, expected_type) in invoice_line_elements.items():
            element = invoice_line.find(relative_path)
            if element is not None and element.text is not None:
                element_text = element.text.strip()

                if element_text == "Please Enter Customer ID (ABN)" or element_text == "Please Enter your account number for payment" \
                    or element_text == "Please Enter your PaymentTerms":
                    validation_result[line_key][key] = 0
                    details[line_key][key] = element_text
                elif element_text and check_type(element_text, expected_type):
                    validation_result[line_key][key] = 1
                    details[line_key][key] = element_text
                else:
                    validation_result[line_key][key] = 0
                    details[line_key][key] = element_text
            else:
                continue


    return validation_result, details