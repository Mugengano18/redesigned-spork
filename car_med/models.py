from django.db import models


# Create your models here.
class Retail_information(models.Model):
    fullname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    city = models.CharField(max_length=30, null=True, blank=True)
    sector = models.CharField(max_length=50, null=True, blank=True)
    cell = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.company_name
