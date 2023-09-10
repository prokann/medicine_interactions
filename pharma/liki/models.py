from django.db import models


class Medicaments(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=60)
    composition = models.CharField(max_length=80)


class Interaction(models.Model):
    remedy_1 = models.CharField(max_length=30)
    remedy_2 = models.CharField(max_length=30)