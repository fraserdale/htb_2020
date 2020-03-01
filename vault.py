from flask import Flask, render_template, request, redirect, jsonify
import random
from datetime import date
from py_tm_vault_client.tmvault.enums import CustomerGender, CustomerTitle
from py_tm_vault_client.tmvault import TMVaultClient
import json 
client = TMVaultClient(
	'/Users/fraserdale/Downloads/py_tm_vault_client_release_0.1.0_team5/data/vault-config.json')


# setup flask app
app = Flask(__name__)

# home index route, returns all the organisations, names and contact details.
@app.route("/create_customer", methods=['POST'])
def create_customer():
	#acc1 = '11dc7693-8b21-9bbe-a428-b29479a4cc27'
	#acc2 = '072b9186-645f-aea0-28e2-b2ae5978eab4'
	#fake_transactions(acc1,acc2)
	#return
	request_information = request.get_json()
	# try:
	
	temp_cust = client.customers.create_customer(
		customer_id=str(random.randint(100000000000000, 999999999999999)),
		# title=CustomerTitle.request_information['personal']['title'],
		first_name=request_information['personal']['firstname'],
		last_name=request_information['personal']['lastname'],
		dob=date(request_information['personal']['dob']['yyyy'], request_information['personal']
					['dob']['mm'], request_information['personal']['dob']['dd']),
		nationality=request_information['personal']['nationality'],
		email_address=request_information['personal']['email'],
		mobile_phone_number=request_information['personal']['phone']
	)

	temp_cust_account = client.accounts.create_account(
		account_id=str(random.randint(1000000000000000, 9999999999999999)),
		# request_information['bank']['type'], #can change later current_account_001
		product_id='current_account',
		stakeholder_customer_ids=[temp_cust.id_],
		with_uk_account_number_and_sort_code=True
		# with_uk_account_number_and_sort_code=True
	)

	#t2 = client.accounts.get_account('154010926358023')

	#a= client.accounts.get_account('154010926358023',True)


	#fake_transactions(temp_cust_account,a)
	print(temp_cust_account)

	return json.dumps({ "id": temp_cust_account.id_ })
	# except:
	#     print('failed')
	#     return {"status": "Error creating account"}



def fake_transactions(acc1, acc2):
	acc1 = client.accounts.get_account(acc1)
	acc2 = client.accounts.get_account(acc2)
	created_payment = client.payments.create_payment(
		amount='10.01',
		currency='GBP',
		debtor_account_id=acc1.id_,
		debtor_sort_code=acc1.uk_sort_code,
		debtor_account_number=acc1.uk_account_number,
		creditor_account_id=acc2.id_,
		creditor_sort_code=acc2.uk_sort_code,
		creditor_account_number=acc2.uk_account_number,
		reference='my first payment',
		metadata={'key': 'value'}
	)
	print('done')


if __name__ == "__main__":
	app.run(port=3001, debug=False)
