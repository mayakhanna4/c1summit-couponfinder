import save
import get
import c_api_calls as coupon
import nessie
from flask import Flask, render_template, redirect, url_for
from firebase_admin import credentials, initialize_app

app = Flask(__name__)
cred = credentials.Certificate("creds/key.json")
initialize_app(cred, {
    'databaseURL': 'https://diamond-a-dozen.firebaseio.com'
})
username = "mjordan"
customer_id = get.user_id(username)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    merchants = nessie.get_merchant_freq(customer_id)
    final_results = {}
    for merchant in merchants:
        merchant_info = nessie.get_merchant_info(merchant)
        merchant_name = merchant_info['name'].encode('utf8').replace(" ", "-")
        list_of_deals = coupon.get_merchant_deals(merchant_name)
        final_results[merchant_name] = {'deals' : list_of_deals, 'id' : merchant }
    return render_template('dashboard.html', final_results = final_results)

@app.route('/popup/<merchant_id>/<deal_id>')
def popup(merchant_id, deal_id):
    deal = coupon.get_deal(deal_id)
    if deal == {}:
        deal = coupon.get_merchant_deals('starbucks')[3]['deal']
    else:
        deal = deal['deal']
    percent_off = coupon.deal_percent_off(deal)
    avg_spent = nessie.get_avg_spent_at_merchant(merchant_id, customer_id)
    dollar_savings =  "$" + str(round(avg_spent * percent_off, 2))
    return render_template('popup.html', deal = deal, savings = dollar_savings)

@app.route('/save/<deal_id>')
def save(deal_id):
    deal = coupon.get_deal(deal_id)
    if deal != {}:
        get.save(username, deal)
    return redirect(url_for("saved"))

@app.route('/saved')
def saved():
    deals = get.get_saved(username)
    deals_list = []
    for deal_id in deals:
        deals_list.append(deals[deal_id])
    print(deals_list)
    return render_template('parse_saved.html', deals = deals_list)
