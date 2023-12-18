from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)


class MedicalKit(models.Model):
    purchase_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(default=timezone.now() + timezone.timedelta(days=363))

    #def save(self, *args, **kwargs):
    #    # 구매 날짜로부터 1년 후의 날짜 계산
    #    if not self.expiration_date:
    #        self.expiration_date = self.purchase_date + relativedelta(years=1)
    #    super().save(*args, **kwargs)

    #def __str__(self):
    #    return f"{self.purchase_date} - {self.expiration_date}"