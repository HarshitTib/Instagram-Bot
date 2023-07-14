import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('instagramFirebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://instagram-bo-default-rtdb.firebaseio.com/'
})
db_ref = db.reference('/')


# print(db_ref.get())

users_ref = db_ref.child('Quotes').child("Walt Disney")

# print(users_ref.get())
# users_ref
# Retrieve the data at the specified path
data = users_ref.get()
# print(data.items())

# # Iterate over the retrieved data
for user_key, user_data in data.items():
  print(user_data)