import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

base_path = os.path.dirname(__file__)
cred = credentials.Certificate(os.path.join(base_path, 'aimanagementTollFirebase.json'))
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user(username: str)-> dict:
    data = db.collection('users')
    docs = data.get()
    for doc in docs:
            return doc.to_dict()

def get_alloted_projects(username: str)-> dict:
    # get the all documents in the collection
    collection = db.collection("projecs")
    docs = collection.get()
    # get the projects that the user has alloted
    projects = []
    for doc in docs:
        if doc.get('alloted_to') == username:
            projects.append(doc.to_dict())
    return db.collection('projects').document(username).collection('alloted_projects').get()

def create_user(user_id: str, username: str, password: str):
    user_data = {
        'username': username,
        'password': password
    }
    db.collection('users').document(user_id).set(user_data)


user_data = get_user('Prabal')
print(user_data)

# get all the collection
collection = db.collection("projects").get()
for doc in collection:
    print(doc.to_dict())


