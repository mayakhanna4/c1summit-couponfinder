from firebase_admin import db
#gets the data from the database

def check(username,password,result):
   ref = db.reference('')
   result = ref.get()
   for user in result:
       if(result[user]["username"] == username and result[user]["password"] == password):
           return


def user_id(username):
   user = db.reference('/' + username).get()
   return user['_id']

#retrive list of deals given user's username
def save(username, deal):
    ref = db.reference('/' + username + '/deal_list');
    ref.update({deal['deal']['id'] : deal['deal']})

#----------------------------
def get_saved(username):
    ref = db.reference('/' + username + '/deal_list')
    return ref.get()


# #sudo pip install requests
# #sudo pip install python-firebase
# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://diamond-a-dozen.firebaseio.com', None)
# result = firebase.get('', None)
# print(result)
# username_1 = "mjordan"
# username_2 = "mkhanna"
# password ="capital"

# check(username_1,password,result)
# check(username_2,password,result)

#print result
