#################################
# NERD_BOT CONNFIGURE VARIABLES #
#################################



#Token
TOKEN = 'TOKEN'


# MongoDB
from pymongo import MongoClient
import os
host = os.environ['OPENSHIFT_MONGODB_DB_HOST']
port   = os.environ['OPENSHIFT_MONGODB_DB_PORT']
mongo_db_local      = MongoClient('mongodb://USERNAME:PASSWORD@%s:%s/' % (host, port)).nerd_bot
mongo_db            = mongo_db_local
mongo_version       = 2


# Save Image Path
find_img_path = './images'
