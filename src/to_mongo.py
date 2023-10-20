from base import Base
import pymongo
import certifi
import os
from dotenv import load_dotenv

class ToMongo(Base):
    '''
    Designed as a class to transport the datat from our Base class to a MongoDB instance
    Initializes an isntance of the inherited class

    Defined methods are as follows:
    upload_one_by_one: Upload piece of info to a database one by one over an iterable structure
    upload_collection: Uploads an entire collection of documents to MongoDB
    delete_collection: Drops an entire collection of data from the database
    '''

    def __init__(self):
        Base.__init__(self)
        load_dotenv()
        self.__mongo_url = os.getenv('MONGO_URL')
        self.client = pymongo.MongoClient(self.__mongo_url, tlsCAFile=certifi.where())
        self.db = self.client.db
        self.cards = self.db.cards
        self.df.set_index('id', inplace=True)

    def upload_one_by_one(self):
        '''
        Upload all our items in the dataframe to MongoDB one-by-one
        This method will take longer, but will ensure all our data is correctly uploaded!
        '''

        for i in self.df.index:
            self.cards.insert_one(self.df.loc[i].to_dict())
        
    def upload_collection(self):
        '''
        Upload an entire collection of documents to MOngoDB.
        BEWARE THERE IS A MAIMUM UPLOAD SIZE!
        Limitations are placed on the amount of data that you can upload at one time!
        '''

        self.cards.insert_many([self.df.to_dict()])

    def drop_collection(self):
        self.db.cards.drop()

if __name__ == '__main__':
    c = ToMongo()
    c.drop_collection()
    print('Dropped Cards Collection')
    c.upload_one_by_one
    print('Successfully Uploaded All Card Info to MongoDB!')