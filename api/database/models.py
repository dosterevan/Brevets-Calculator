from mongoengine import *


class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        km/miles: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine string field, required, (checkpoint opening time),
		close_time: MongoEngine string field, required, (checkpoint closing time).
    """
    km = FloatField(required=True)
    miles = FloatField(required=True)
    location = StringField()
    open_time = StringField(required=True)
    close_time = StringField(required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
		distance: MongoEngine float field, required
		begin_date: MongoEngine string field, required
		controls: MongoEngine list field of Checkpoints, required
    """
    distance = FloatField(required=True) 
    begin_date = StringField(required=True)
    controls = ListField(EmbeddedDocumentField(Checkpoint), required=True)
