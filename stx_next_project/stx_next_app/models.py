from django.db import models


class Book(models.Model):
    title = models.TextField()
    authors = models.TextField()
    published_date = models.DateTimeField()
    page_count = models.IntegerField()
    image_links = models.ForeignKey('ImageLinks', on_delete=models.DO_NOTHING)
    language = models.CharField(max_length=10)


class IndustryIdentifiers(models.Model):
    type = models.TextField()
    identifier = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING)


class ImageLinks(models.Model):
    small_thumbnail = models.URLField()
    thumbnail = models.URLField()
    small = models.URLField()
    medium = models.URLField()
    large = models.URLField()
    extraLarge = models.URLField()