import os
from pathlib import Path

LOCAL = "local"
PROD = "prod"
SOZIN = 'sozin'
# -> MASTER PATH <- #
master_path = os.getcwd()

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

USERAGENTS = os.path.join(get_parent_directory(), 'FWEB/fwebResources/useragents.txt')

"""
docker run --name tiffany-mongo4 -v /mnt/SozinData/docker/TiffanyMongo:/data/db -d mongo:4.4
"""

""" -> SERVER INFO <- """
db_environment = "sozin"

local_mongo_ip = "localhost"
local_mongo_port = "27017"
local_mongo_db_uri = 'mongodb://{0}:{1}'.format(local_mongo_ip, local_mongo_port)

# prod_mongo_ip = env.get_env("PROD_MONGO_IP")
# prod_mongo_port = env.get_env("PROD_MONGO_PORT")
# prod_mongo_password = env.get_env("PROD_MONGO_PASSWORD")
# prod_mongo_db_uri = 'mongodb://{0}:{1}'.format(prod_mongo_ip, prod_mongo_port)
#
sozin_mongo_ip = "192.168.1.180"
sozin_mongo_port = "27017"
sozin_mongo_password = ""
sozin_mongo_db_uri = 'mongodb://{0}:{1}'.format(sozin_mongo_ip, sozin_mongo_port)