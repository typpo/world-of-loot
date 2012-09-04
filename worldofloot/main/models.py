from django.db import models
from django.contrib.auth.models import User
import tagging

class Item(models.Model):
  item_id = models.CharField(max_length=10)
  item_type = models.CharField(max_length=30)   # gear or mount

  name = models.CharField(max_length=75)
  ilvl = models.IntegerField(default=-1)
  quality = models.CharField(max_length=20, null=True) # TODO convert to select
  icon = models.CharField(max_length=20, null=True)
  slot = models.CharField(max_length=20, null=True) # TODO convert to select

  wants = models.IntegerField(default=0)
  haves = models.IntegerField(default=0)

  def __unicode__(self):
    return 'Item %s' % (self.name)

class Pin(models.Model):
  item = models.ForeignKey(Item)
  user = models.ForeignKey(User, null=True)
  session = models.CharField(max_length=60, null=True)
  verb = models.CharField(max_length=10) # TODO convert to select

  def __unicode__(self):
    return 'Pin of %s by %s' % (self.item.name, self.user.email)

class Image(models.Model):
  item = models.ForeignKey(Item)
  image_id = models.CharField(primary_key=True, max_length=20)
  path = models.CharField(max_length=200)
  thumb_path = models.CharField(max_length=200)
  attribution = models.CharField(max_length=25)

  priority = models.IntegerField()  # lower is better

  def __unicode__(self):
    return 'Image for %s' % (self.item.name)

"""
# Introspection rules for south
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tagging\.fields\.TagField"])
except ImportError:
    pass
"""
