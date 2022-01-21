from pymongo import MongoClient

client = MongoClient("mongodb://root:example@172.23.144.1:8081/?authSource=admin")

db = client.authn

collection = db.collection

cursor = collection.find({})
for document in cursor:
        print(document)