import pymongo

from backbone.configs import config

MONGODB_CLIENT = pymongo.MongoClient(
    "mongodb://%s:%s@%s" % (config.MONGODB_USERNAME, config.MONGODB_PASSWORD, config.MONGODB_URL))


def get_mongo_client():
    return MONGODB_CLIENT
