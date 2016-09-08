from django.db import models

# Create your models here.
class TUser(models.Model):

    screen_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    favorites_count = models.IntegerField()
    followers_count = models.IntegerField()
    friends_count = models.IntegerField()
    twitter_id = models.IntegerField()
    statuses_count = models.IntegerField()

    created_at = models.DateTimeField()

    time_zone = models.CharField(max_length=250, null=True)
    lang = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=250, null=True)

class Hashtag(models.Model):

    text = models.CharField(max_length=250)

class Media(models.Model):

    url = models.URLField()
    display_url = models.URLField()
    media_url = models.URLField()
    type = models.CharField(max_length=250)

class URL(models.Model):

    url = models.URLField()
    display_url = models.URLField()
    expanded_url = models.URLField()

class Tweet(models.Model):
    hashtags = models.ManyToManyField(Hashtag)
    media = models.ManyToManyField(Media)
    # symbols = models.ManyToManyField()
    urls = models.ManyToManyField(URL)
    user_mentions = models.ManyToManyField(TUser, related_name='mentions')

    created_at = models.DateTimeField()
    favorite_count = models.IntegerField()
    twitter_id = models.IntegerField()

    in_reply_to_screen_name = models.CharField(max_length=250, null=True)
    in_reply_to_user_id = models.IntegerField(null=True)

    is_quote_status = models.BooleanField()
    retweet_count = models.IntegerField()
    retweeted = models.BooleanField()

    text = models.CharField(max_length=250)
    timestamp_ms = models.IntegerField()
    user = models.ForeignKey(TUser, related_name='tweets')
    lang = models.CharField(max_length=10)

    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)