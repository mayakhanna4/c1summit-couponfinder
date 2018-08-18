import requests
import json

api_key = "htCoKmVm"
domain = 'https://api.discountapi.com/v2/deals'

def url_str(call_str):
    return domain + call_str +'api_key=' + api_key

def get_merchant_deals(merchant_name):
    url = url_str('?query={}&'.format(merchant_name))
    response = requests.get(url)
    print(response.status_code)
    if response.status_code != 200:
        # some kind of error reponse
        print("Error getting Deals")
        print(response.json())
        return []
    py_obj = (response.json())
    deal_list = py_obj["deals"]
    #for deal in deal_list:
        #print deal["deal"]["merchant"]["name"]
        #print' '
    return deal_list


def get_deal(deal_id):
    url = url_str('/' + deal_id + "/?")
    res = requests.get(url)
    if res.status_code != 200:
        return {}
    return res.json()

def get_deal_image_url(id):
    url = url_str('/{}/image?'.format(id))
    return url

# given a deal object from the discount api return the percent off
def deal_percent_off(deal):
    print("percent off")
    print(deal)
    return deal['price'] / deal['value']

# given a deal object from the discount api return the hard dollar amount off
def deal_dollars_off(deal):
    return deal['discount_amount']
