from mongoengine import *


class Checkpoint(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        km/miles: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    km = FloatField(required=True)
    miles = FloatField(required=True)
    location = StringField()
    open_time = DateTimeField(required=True)
    close_time = DateTimeField(required=True)


class Brevet(Document):
    """
    A MongoEngine document containing:
		distance: MongoEngine float field, required
		begin_date: MongoEngine datetime field, required
		controls: MongoEngine list field of Checkpoints, required
    """
    distance = FloatField(required=True) 
    begin_date = DateTimeField(required=True)
    controls = ListField(EmbeddedDocumentField(Checkpoint), required=True)
