from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity1 = models.IntegerField(default=0)
    quantity2 = models.IntegerField(default=0)
    quantity3 = models.IntegerField(default=0)
    


class MedicalKit(models.Model):
    purchase_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    expiration_date1 = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.purchase_date and not self.expiration_date:
            self.expiration_date = self.purchase_date + relativedelta(days=365)
        super().save(*args, **kwargs)


class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

class ArduinoData(models.Model):
    data = models.CharField(max_length=255)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    