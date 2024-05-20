
import json


# To fix collections error in Authorize.NET source code
import collections 
import collections.abc
collections.MutableSequence = collections.abc.MutableSequence

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *


def get_credit_card(*, card_number="4111111111111111",
                       expiration_date="2035-12", card_code="123"):
    """
    Get the payment data for a credit card

    Args:
        card_number (str, optional): Defaults to "4111111111111111".
        expiration_date (str, optional): Defaults to "2035-12".
        card_code (str, optional): Defaults to "123".

    Disclaimer: default values are for rapid testing only, and code shouldn't be shipped with them.

    Returns:
        credit_card: creditCardType obj
    """
    credit_card = apicontractsv1.creditCardType()
    credit_card.cardNumber = card_number
    credit_card.expirationDate = expiration_date
    credit_card.cardCode = card_code
    
    return credit_card


def get_customer_address(*, first_name="Ellen", last_name="Johnson", company="Souveniropolis",
                         address="14 Main Street", city="Pecan Springs", state="TX", zip_code="44628", country="USA"):
    """
    Get customer's address used for Billing

    Args:
        first_name (str, optional): Customer's first name. Defaults to "Ellen".
        last_name (str, optional): Customer's last name. Defaults to "Johnson".
        company (str, optional):  Defaults to "Souveniropolis".
        address (str, optional):  Defaults to "14 Main Street".
        city (str, optional):  Defaults to "Pecan Springs".
        state (str, optional):  Defaults to "TX".
        zip_code (str, optional):  Defaults to "44628".
        country (str, optional):  Defaults to "USA".

    Disclaimer: default values are for rapid testing only, and code shouldn't be shipped with them.

    Returns:
        customer_address: customerAddressType obj
    """
    customer_address = apicontractsv1.customerAddressType()
    customer_address.firstName = first_name
    customer_address.lastName = last_name
    customer_address.company = company
    customer_address.address = address
    customer_address.city = city
    customer_address.state = state
    customer_address.zip = zip_code
    customer_address.country = country
    
    return customer_address


def get_customer_data(*, customer_type="individual", customer_id="99999456654", customer_email="EllenJohnson@example.com"):
    """
    Set the customer's identifying information

    Args:
        customer_type (str, optional):  Defaults to "individual".
        customer_id (str, optional):  Defaults to "99999456654".
        customer_email (str, optional):  Defaults to "EllenJohnson@example.com".

    Disclaimer: default values are for rapid testing only, and code shouldn't be shipped with them.

    Returns:
        customer_data: customerDataType obj
    """
    customer_data = apicontractsv1.customerDataType()
    customer_data.type = customer_type
    customer_data.id = customer_id
    customer_data.email =  customer_email
    
    return customer_data


def create_order_items():
    """
    Create order information

    Returns:
        order: orderType
    """
    # Create order information
    order = apicontractsv1.orderType()
    order.invoiceNumber = "10101"
    order.description = "Golf Shirts"
    
    return order



def create_list_items():
    """
    Setup individual line items from mock data

    Returns:
        line_items: ArrayOfLineItem
    """
    line_items = apicontractsv1.ArrayOfLineItem()
    with open("data/items.json") as items:
        order_items = json.load(items)
        for order_item in order_items:
            line_item = apicontractsv1.lineItemType()
            for item_key, item_val in order_item.items():
                setattr(line_item, item_key, item_val)
            line_items.lineItem.append(line_item)
    
    return line_items


def seed_payment_data(credit_card):
    """
    

    Args:
        credit_card (apicontractsv1.creditCardType): customer's credit card data

    Returns:
        payment: paymentType obj
    """
    payment = apicontractsv1.paymentType()
    payment.creditCard = credit_card
    
    return payment


def set_payments_settings():
    """
    setup transaction settings

    Returns:
        settings: settingType
    """
    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings = apicontractsv1.ArrayOfSetting()
    settings.setting.append(duplicateWindowSetting)
    
    return settings


def handle_credit_card_charging(response):
    """
    Handle reponse sent to user in case of succcess or failure of transaction

    Args:
        response (dict): response transaction attempt to be jsonified later

    Returns:
        response_obj: dict
    """
    response_obj = dict()
    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":
            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages'):
                response_obj["message"] = 'Successfully created transaction with' \
                    f'Transaction ID {str(response.transactionResponse.transId)}'
                response_obj["transaction_code"] = str(response.transactionResponse.responseCode)
                response_obj["message_code"] = str(response.transactionResponse.messages.message[0].code)
                response_obj["description"] = str(response.transactionResponse.messages.message[0].description)
            else:
                response_obj["message"] = 'Failed Transaction.'
                if hasattr(response.transactionResponse, 'errors'):
                    response_obj["error_code"] = str(response.transactionResponse.errors.error[0].errorCode)
                response_obj["error_message"] = str(response.transactionResponse.errors.error[0].errorText)
        else:
            print('Failed Transaction.')
            if hasattr(response, 'transactionResponse') and hasattr(
                    response.transactionResponse, 'errors'):
                response_obj["error_code"] = str(response.transactionResponse.errors.error[0].errorCode)
                response_obj["error_message"] = str(response.transactionResponse.errors.error[0].errorText)

            else:
                response_obj["error_code"] = str(response.messages.message[0]['code'].text)
                response_obj["error_message"] = str(response.messages.message[0]['text'].text)
    else:
        response_obj["message"] = None
        
    return response_obj
