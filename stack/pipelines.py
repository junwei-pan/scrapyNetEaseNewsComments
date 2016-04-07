import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        #self.collection = db[settings['MONGODB_COLLECTION']]
        self.dict_itemName_collectionName = {
            'ItemComments': 'comments',
            'ItemNews': 'newsContent',
            }
        self.db['comments'].create_index([("commentId", pymongo.ASCENDING)], unique = True)
        self.db['newsContent'].create_index([("newsId", pymongo.ASCENDING)], unique = True)

    def process_item(self, item, spider):
        self.collection = self.db[self.dict_itemName_collectionName[type(item).__name__]]
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
