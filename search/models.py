from django.db import models


class Word(models.Model):
    word_text = models.CharField(max_length=50)

class Website(models.Model):
    title_text = models.CharField(max_length=100)
    link_text = models.CharField(max_length=10000)
    word = models.ManyToManyField(Word, through='WordWebsite')

class WordWebsite(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
