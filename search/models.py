from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50, default=None, db_index=True)

class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=10000)
    root = models.ForeignKey('self', default=None, on_delete=models.CASCADE)
    word = models.ManyToManyField(Word, through='WordWebsite')

class WordWebsite(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
