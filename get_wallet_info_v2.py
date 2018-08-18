import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

#retrive list of deals given user's username
def save(username, deal):
    ref = db.reference('/' + username + '/deal_list');
    ref.update({deal['deal']['id'] : deal['deal']})

#----------------------------
def get_saved(username):
    ref = db.reference('/' + username + '/deal_list')
    return ref.get()

