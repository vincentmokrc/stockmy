import mongoengine as mg
from pymongo import MongoClient

class DatabaseMongo:
    def __init__(self, db_name, ip_address, port = 27017, item_object = None):
        self.client = MongoClient('192.168.1.130', 27017)
        self.db_name = db_name
        self.item_object = item_object

    def insert(self):
        db = self.client[self.db_name]
        posts = db.posts
        post_data = {
            'date': self.item_object.Date,
            'Foreign': {'Bought' : self.item_object.Foreign_Bought , 'Sold' : self.item_object.Foreign_Sold},
            'Local_Institution': {'Bought' : self.item_object.Local_Institution_Bought , 'Sold' : self.item_object.Local_Institution_Sold},
            'Local_Retail' : {'Bought' : self.item_object.Local_Retail_Bought , 'Sold' : self.item_object.Local_Retail_Sold}
        }
        result = posts.insert_one(post_data)
        print('One post: {0}'.format(result.inserted_id))



class TradingParticipation(mg.Document):
    Date = mg.StringField(unique=True)
    Foreign_Bought = mg.DecimalField()
    Foreign_Sold = mg.DecimalField()
    Local_Institution_Bought = mg.DecimalField()
    Local_Institution_Sold = mg.DecimalField()
    Local_Retail_Bought = mg.DecimalField()
    Local_Retail_Sold = mg.DecimalField()

if __name__ == "__main__":
    client = MongoClient('192.168.1.130', 27017)
    db = client['pymongo_test']
    posts = db.posts
    post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

