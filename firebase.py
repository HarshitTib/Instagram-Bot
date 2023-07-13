import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


#Firebase Authentication
cred = credentials.Certificate('instagramFirebase.json')
firebase_admin.initialize_app(cred)

#Firebase Configuration
firebaseConfig = {
  "apiKey": "AIzaSyDkL-a-xpid_CyZhjYcRfI_1XM3f8bSGjY",
  "authDomain": "instagram-bo.firebaseapp.com",
  "databaseURL": "https://instagram-bo-default-rtdb.firebaseio.com/",
  "projectId": "instagram-bo",
  "storageBucket": "instagram-bo.appspot.com",
  "messagingSenderId": "258408664102",
  "appId": "1:258408664102:web:67bc4621dd9b5972992ae7",
  "measurementId": "G-N2YELNELVH"
} 



#Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#push the data
data = "Beleieve you can and you're halfway there"

db.child("Quotes").child("Theodre Roosevelt").push(data)
# db.child("Quotes").child("Theodre Roosevelt").push(data)
# db.child("Quotes").child("Theodre Roosevelt").set(data)
# db.child("Quotes").child("Theodre Roosevelt").set(data)


#retreive the data

datas = db.child("Quotes").child("Theodre Roosevelt").get()
# print(datas.val())
# print(len(datas.val()))
for i in datas.each():
  print(i.val())



#to remove the data
db.remove() 