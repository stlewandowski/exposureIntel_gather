from pymongo import MongoClient
import configparser

# config parser
config = configparser.ConfigParser()
config.read('conf.ini')
mongo_user = config['Mongo']['user']
mongo_pass = config['Mongo']['pass']
mongo_server = config['Mongo']['server']
mongo_replica = config['Mongo']['replica']
mongo_db = config['Mongo']['db']

c = MongoClient(mongo_server, username=mongo_user, password=mongo_pass, authSource=mongo_db)
print(c)
info = c.server_info()
print(info)
db = c[mongo_db]
coll = db.test
res = coll.find_one()
print(res)
