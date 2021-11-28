from django.contrib.auth.models import User
from django.db import models


class Ksiazka(models.Model):
    indeks = models.AutoField(primary_key=True)
    tytul = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    rok_wydania = models.IntegerField()
    wydawnictwo = models.CharField(max_length=200)
    posiadacz = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
