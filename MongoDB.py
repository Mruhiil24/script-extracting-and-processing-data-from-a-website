import db as db
import pandas as pd
import pymongo
from pymongo import MongoClient

df = open('/Users/monekaruhiil/PycharmProjects/selenium/article_text.txt')

client =  MongoClient("mongodb+srv://moneka:Moneka2019!@cluster0.zgi2n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['dev']
collection = db['NewsScraping']

data.reset_index(inplace=True)

data_dict = data.to_dict("records")

# Insert collection
collection.insert_many(data_dict)
