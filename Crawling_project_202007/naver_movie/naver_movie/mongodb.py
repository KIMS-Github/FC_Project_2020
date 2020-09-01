import pymongo

client = pymongo.MongoClient('mongodb://test:pw@13.124.183.209:27017')
db = client.naver_movie
collection = db.items
