import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin with service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
