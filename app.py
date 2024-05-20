from flask import Flask, request, jsonify

# To fix collections error in Authorize.NET source code
import collections
collections.MutableSequence = collections.abc.MutableSequence


from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *

from constants import API_LOGIN_ID, TRANSACTION_KEY, MERCHANT_REF_ID
from utils import *



app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Try hitting /accept-payment endpoint to test out the task.</p>"


@app.route("/accept-payment", methods=['POST'])
def accept_payment():
    
    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_LOGIN_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    amount = request.json.get("amount")
    credit_card = get_credit_card()
    

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = seed_payment_data(credit_card)
    transactionrequest.order = create_order_items()
    transactionrequest.billTo = get_customer_address()
    transactionrequest.customer = get_customer_data()
    transactionrequest.transactionSettings = set_payments_settings()
    transactionrequest.lineItems = create_list_items()
    
    
    # # Assemble the complete transaction request
    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = MERCHANT_REF_ID
    createtransactionrequest.transactionRequest = transactionrequest
    # Create the controller
    createtransactioncontroller = createTransactionController(
        createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()
    
    content = handle_credit_card_charging(response)
    return jsonify(content)



if __name__ == "__main__":

    app.run(debug=True)
