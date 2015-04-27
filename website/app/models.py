from django.db import models


class NewsHeadline(models.Model):
    text = models.CharField(max_length=400)
    time_stamp = models.CharField(max_length=200)


class Price(models.Model):
    from django.core.validators import MaxValueValidator, MinValueValidator
    value = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(100.0)])
    time_stamp = models.CharField(max_length=200)