from django.db import models

DATE_FORMATS = ['%Y-%m-%d','%Y']

class Book(models.Model):
    title = models.TextField()
    published_date = models.DateField(null=True)
    page_count = models.IntegerField(null=True)
    image_links = models.ForeignKey('ImageLinks', on_delete=models.DO_NOTHING, null=True)
    language = models.CharField(max_length=10)


class Authors(models.Model):
    author = models.CharField(max_length=100)
    book = models.ManyToManyField('Book', through='BookAuthors')


class BookAuthors(models.Model):
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey('Authors', on_delete=models.DO_NOTHING, null=True)


class IndustryIdentifiers(models.Model):
    type = models.TextField()
    identifier = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.DO_NOTHING, null=True)


class ImageLinks(models.Model):
    small_thumbnail = models.URLField()
    thumbnail = models.URLField()
    small = models.URLField()
    medium = models.URLField()
    large = models.URLField()
    extra_large = models.URLField()