#Saves the data to the database


#Import databse module
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials


def save_info(username,password,first_name,last_name):
    cred = credentials.Certificate('serviceAccountKey.json')
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://diamond-a-dozen.firebaseio.com',
        'databaseAuthVariableOverride': None
    })
    ref = db.reference();
    users_ref = ref.child('users')
    users_ref.set({
        username: {
            'username': username,
            'password':password,
            'first_name':first_name,
            'last_name':last_name
        }
    })
def login(username,password):
    username = "mjordan"
    password = "capital"
