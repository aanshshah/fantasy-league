from __future__ import unicode_literals

from django.db import models
import ast
# from gdstorage.storage import GoogleDriveStorage
from s3direct.fields import S3DirectField

# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class Player(models.Model):
    user = models.ForeignKey('auth.User')
    first_name = models.CharField(max_length=256, default=None)
    last_name = models.CharField(max_length=256, default=None)
    rating = models.IntegerField()
    league = models.ForeignKey('League', default=None)
    #name each picture the same as the player id 
    picture = S3DirectField(dest='example3')


class League(models.Model):
    name = models.CharField(max_length=256)
    special_users = models.ForeignKey('SpecialUser', default=None)
    players = models.ManyToManyField('auth.User')
    password = models.CharField(max_length=256, default=None)
    last_game = models.DateTimeField(default=None, null=True, blank=True)
    games_in_season = models.IntegerField(default=7, null=True, blank=True)
    duration_between_games = models.IntegerField(default=7, null=True, blank=True)
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    pairings = ListField(default=None, null=True, blank=True)

class SpecialUser(models.Model):
    user = models.ForeignKey('auth.User')
    admin = models.BooleanField(default=False)
    rater = models.BooleanField(default=False)

class Trade_Notification(models.Model):
    user_requesting_trade = models.ForeignKey('auth.User')
    player_traded = models.ManyToManyField('Player')
    date_requested = models.DateTimeField()
    date_accepted = models.DateTimeField(default=None)
    trade_status = models.BooleanField(default=False) #used for trade history
    notification_active = models.BooleanField(default=True) #used for trade notifications
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

class History(models.Model):
    user = models.ForeignKey('auth.User')
    league = models.ForeignKey('League')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    current_ranking = models.IntegerField(default=0)

class Match_Pairings(models.Model):
    users = models.ManyToManyField('auth.User')
    league = models.ForeignKey('League')
    details = models.ManyToManyField('User_Match_Details', default=None)
    number = models.IntegerField(default=0)


class User_Match_Details(models.Model):
    match_number = models.IntegerField(default=0)
    user = models.ForeignKey('auth.User', default=None)
    total_points = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    tie = models.BooleanField(default=False)
    match_pairing = models.ForeignKey('Match_Pairings', default=None)
    bye = models.BooleanField(default=False)
