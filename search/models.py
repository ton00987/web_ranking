from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50, default=None, db_index=True)

class Website(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=10000)
    date = models.DateField(default='2000-01-01')
    click = models.IntegerField(default=0)
    ref = models.ManyToManyField('self', default=None, null=True, symmetrical=False, db_index=True)
    word = models.ManyToManyField(Word, through='Have')

class Have(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    
