from django.contrib.auth.models import User
from django.db import models

__all__ = ['UniwallUser', 'Pictures', 'Entry', 'Event', 'Subscribers']


class EntryManager(models.Manager):
    def get_uni_entries(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        return self.filter(user__school=uni_user.school).order_by('-id')


class PicturesManager(models.Manager):
    def get_uni_pictures(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        return self.filter(user__school=uni_user.school).order_by('-id')


class EventManager(models.Manager):
    def get_uni_events(self, user):
        uni_user = UniwallUser.objects.get(user=user)
        return self.filter(organizator__school=uni_user.school).order_by('-id')


class UniwallUser(models.Model):
    user = models.OneToOneField(User)
    school = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username


class Pictures(models.Model):
    user = models.ForeignKey(UniwallUser)
    content = models.FileField(upload_to='pictures')
    time = models.DateTimeField(auto_now=True)
    objects = PicturesManager()


class Entry(models.Model):
    user = models.ForeignKey(UniwallUser)
    content = models.TextField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    objects = EntryManager()

    def __unicode__(self):
        return self.content


class Event(models.Model):
    organizator = models.ForeignKey(UniwallUser)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    objects = EventManager()


class Subscribers(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(UniwallUser)
