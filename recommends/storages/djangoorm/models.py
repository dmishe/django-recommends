from django.db import models
from django.contrib.contenttypes import generic
from .managers import RecommendsManager, SimilarityManager, RecommendationManager


class RecommendsBaseModel(models.Model):
    """(RecommendsBaseModel description)"""
    object_ctype = models.PositiveIntegerField()
    object_id = models.PositiveIntegerField()
    object_site = models.PositiveIntegerField()
    object = generic.GenericForeignKey('object_ctype', 'object_id')

    objects = RecommendsManager()

    class Meta:
        abstract = True
        unique_together = ('object_ctype', 'object_id', 'object_site')

    def __unicode__(self):
        return u"RecommendsBaseModel"


class Similarity(RecommendsBaseModel):
    """How much an object is similar to another"""

    score = models.FloatField(null=True, blank=True, default=None)

    related_object_ctype = models.PositiveIntegerField()
    related_object_id = models.PositiveIntegerField()
    related_object_site = models.PositiveIntegerField()
    related_object = generic.GenericForeignKey('related_object_ctype', 'related_object_id')

    objects = SimilarityManager()

    class Meta:
        verbose_name_plural = 'similarities'
        unique_together = ('object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site')
        ordering = ['-score']

    def __unicode__(self):
        return u"Similarity between %s and %s" % (self.object, self.related_object)


class Recommendation(RecommendsBaseModel):
    """Recommended an object for a particular user"""
    user = models.PositiveIntegerField()
    score = models.FloatField(null=True, blank=True, default=None)

    objects = RecommendationManager()

    class Meta:
        unique_together = ('object_ctype', 'object_id', 'user')
        ordering = ['-score']

    def __unicode__(self):
        return u"Recommendation for user %s" % (self.user)
