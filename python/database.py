###
# 기능설명 : mysql, mongoDB연결
# 작성자명 : 송한나
# 작성일자 : 2024.05.01
###
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from pymongo import mongo_client
import os.path
import json

# SECREAT.JSON 연결
BASE_DIR = os.path.dirname(os.path.relpath("./"))
secret_file = os.path.join(BASE_DIR, 'secret.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg
    
# MYSQL
HOSTNAME = get_secret("Mysql_Hostname")
PORT = get_secret("Mysql_Port")
USERNAME = get_secret("Mysql_Username")
PASSWORD = get_secret("Mysql_Password")
DBNAME = get_secret("Mysql_DBname")
DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DBNAME}'

class Mysql_conn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session
    
    def connection(self):
        conn = self.engine.connection()
        return conn

#MONGODB
MONGOHOSTNAME = get_secret("Local_Mongo_Hostname")
MONGOUSERNAME = get_secret("Local_Mongo_Username")
MONGOPASSWORD = get_secret("Local_Mongo_Password")

client = mongo_client.MongoClient(f'mongodb://{MONGOUSERNAME}:{MONGOPASSWORD}@{MONGOHOSTNAME}')
mydb = client['findtheshop']
mycol = mydb['lowlink']




