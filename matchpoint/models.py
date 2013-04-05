from mongoalchemy import fields
from mongoalchemy.document import Document


class Match(Document):
    domains = fields.ListField(fields.StringField())
    keywords = fields.ListField(fields.StringField())


class InterestVersion(Document):
    modified = fields.DateTimeField()
    duration = fields.IntField()
    threshold = fields.IntField()
    matches = fields.ListField(fields.DocumentField(Match))


class Interest(Document):
    name = fields.StringField()
    modified = fields.DateTimeField()
    current = fields.DocumentField(InterestVersion)
    versions = fields.ListField(fields.DocumentField(InterestVersion))


class Namespace(Document):
    name = fields.StringField()
    modified = fields.DateTimeField()
    interests = fields.ListField(fields.DocumentField(Interest))

    def __unicode__(self):
        return u'<Namespace: %s>' % self.name
