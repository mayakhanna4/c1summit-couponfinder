import requests
import json

api_key = 'a824346586730c06544e3494b2742078'
domain = 'http://api.reimaginebanking.com'

def url_str(call_str):
    return domain + call_str + '?key=' + api_key


def valid_response(fcn, res):
    if res.status_code != 200:
        # some kind of error repsonse
        print(fcn + " error")
        print(res.json())
        return False
    return True

def get_account_ids(customer_id):
    url = url_str('/customers/{}/accounts'.format(customer_id))
    response = requests.get(url)
    if not valid_response("get_account_ids", response):
        return []
    account_ids = list(map(lambda a : a['_id'], response.json()))
    return account_ids


def get_purchases(account_id):
    url = url_str('/accounts/{}/purchases'.format(account_id))
    res = requests.get(url)
    if not valid_response("get_purchases", res):
        return []
    return res.json()

# this is used to populate the card info on dashboard.html
# returns a dict of:
# > id (string)
# > name (string)
# > categories (list)
# > geocode (dict of long + latitude)
# > address (dict)
def get_merchant_info(merchant_id):
    url = url_str('/merchants/{}'.format(merchant_id))
    res = requests.get(url)
    if not valid_response("get_merchant_info", res):
        return {}
    return res.json()

def get_purchases_at_merchant(merchant_id, account_id):
    url = url_str('/merchants/{}/accounts/{}/purchases'.format(
        merchant_id, account_id))
    res = requests.get(url)
    if not valid_response("get_merchant_info", res):
        return {}
    return res.json()

def get_total_spent_at_merchant(merchant_id, customer_id):
    accounts = get_account_ids(customer_id)
    total = 0
    for account in accounts:
        purchases = get_purchases_at_merchant(merchant_id, account)
        for purchase in purchases:
            total += purchase['amount']
    return total

# returns a number of avg $ spent at merchant
def get_avg_spent_at_merchant(merchant_id, customer_id):
    accounts = get_account_ids(customer_id)
    total = 0
    num_purchases = 0
    for account in accounts:
        purchases = get_purchases_at_merchant(merchant_id, account)
        num_purchases += len(purchases)
        for purchase in purchases:
            total += purchase['amount']
    return total / num_purchases

#overview page
# Returns dictionary with merchant ids as keys and frequency as values
def get_merchant_freq(customer_id):
    purchase_freq = {}
    accounts = get_account_ids(customer_id)
    for account in accounts:
        purchases = get_purchases(account)
        for p in purchases:
            merchant_id = p['merchant_id']
            purchase_freq[merchant_id] = purchase_freq.get(merchant_id, 0) + 1
    return purchase_freq
