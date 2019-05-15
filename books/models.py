from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=100)
    description = models.TextField()
    api_key = models.CharField(max_length=50, null=True, blank=True)
    thumbnail = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
