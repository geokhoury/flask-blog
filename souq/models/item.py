from mongoengine import *
from mongoengine.fields import DateField
from wtforms.validators import Required
from .comment import Comment
from .user import User
from datetime import datetime

class Item(Document):
    # define class metadata
    meta = {'collection': 'items', 'allow_inheritance': True}
    # define class fields
    title = StringField(max_length=120, required=True)
    store_name = ReferenceField(User,reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(default=datetime.now())
    price = FloatField(required = True)
    quantity= IntField(required = True)
    selling_price = FloatField(required = True)

    def get_by_item(cls, item_id):
        data = Item.objects.get(id = str(item_id))
        if data is not None:
            return data

    
    
class TextItem(Item):
    content = StringField()


class ImageItem(Item):
    image_path = StringField()


class LinkItem(Item):
    link_url = StringField()
