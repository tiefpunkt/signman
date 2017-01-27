from peewee import *
from datetime import datetime
from config import *

db = SqliteDatabase(DB_DATA_DIR)


class BaseModel(Model):
    class Meta:
        database = db


class URL(BaseModel):
    url = CharField()
    duration = IntegerField()
    is_active = BooleanField()

    def __unicode__(self):
        return self.url


class Sign(BaseModel):
    token = CharField(unique=True)
    name = CharField()
    last_url = ForeignKeyField(URL, null=True)
    last_url_first_send = DateTimeField(null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.token)

    def activeURLs(self):
        urls = []
        for url in URL.select().join(SignURL).where(SignURL.sign == self, SignURL.is_active == True,
                                                    URL.is_active == True):
            urls.append(url.url)
        return urls

    def getCurrentURL(self):
        if not self.last_url:
            url = URL.select().join(SignURL).where(SignURL.sign == self, SignURL.is_active == True,
                                                   URL.is_active == True).get()
            self.last_url = url
            self.last_url_first_send = datetime.now()
            self.save()
        else:
            delta = datetime.now() - self.last_url_first_send

            if delta.total_seconds() > self.last_url.duration * 60:
                # new URL
                try:
                    url = URL.select().join(SignURL).where(SignURL.sign == self, SignURL.is_active == True,
                                                           URL.is_active == True, URL.id > self.last_url.id).get()
                except:
                    url = URL.select().join(SignURL).where(SignURL.sign == self, SignURL.is_active == True,
                                                           URL.is_active == True).get()
                self.last_url = url
                self.last_url_first_send = datetime.now()
                self.save()
            else:
                url = self.last_url
        return url.url


class SignURL(BaseModel):
    sign = ForeignKeyField(Sign, related_name='urls')
    url = ForeignKeyField(URL, related_name='signs')
    is_active = BooleanField()


db.connect()
db.create_tables([URL, Sign, SignURL], True)
