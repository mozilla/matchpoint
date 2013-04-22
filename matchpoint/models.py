import os

from mongoalchemy import fields
from mongoalchemy.document import Document
from mongoalchemy.session import Session


# TODO: Move to matchpoint.models.base
class DocumentBase(Document):
    """Base class with useful methods."""

    def __unicode__(self):
        return u'<%s>' % self.__class__.__name__

    def to_dict(self):
        raise NotImplemented()

    def save(self):
        s = Session.connect('default')  # XXX
        return s.insert(self)

    @classmethod
    def query(cls):
        host = os.getenv('MONGODB_URL', 'localhost')
        s = Session.connect('default', host)  # XXX
        return s.query(cls)


class Match(DocumentBase):
    domains = fields.ListField(fields.StringField())
    keywords = fields.ListField(fields.StringField())


    def to_dict(self):
        return {
            'domains': self.domains,
            'keywords': self.keywords,
        }


class InterestVersion(DocumentBase):
    modified = fields.DateTimeField()
    duration = fields.IntField()
    threshold = fields.IntField()
    matches = fields.ListField(fields.DocumentField(Match))

    def to_dict(self):
        return {
            'duration': self.duration,
            'threshold': self.threshold,
            'matches': [m.to_dict() for m in self.matches],
        }


class Interest(DocumentBase):
    name = fields.StringField()
    modified = fields.DateTimeField()
    current = fields.DocumentField(InterestVersion)
    versions = fields.ListField(fields.DocumentField(InterestVersion))

    def to_dict(self):
        if self.current:
            return self.current.to_dict()
        return None


class Namespace(DocumentBase):
    name = fields.StringField()
    modified = fields.DateTimeField()
    interests = fields.ListField(fields.DocumentField(Interest))
    removed = fields.BoolField()

    def __unicode__(self):
        return u'<Namespace: %s>' % self.name
