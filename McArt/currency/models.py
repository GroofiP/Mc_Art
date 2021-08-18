from django.db import models


class Currency(models.Model):
    translate_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    nominal = models.PositiveSmallIntegerField()
    parent_code = models.CharField(max_length=32)
    iso_num = models.CharField(max_length=16)
    iso_char = models.CharField(max_length=16)

    def __str__(self):
        return self.translate_name


class SumDate(models.Model):
    sum_date_1 = models.FloatField(null=True, blank=True, default=0)
    sum_date_2 = models.FloatField(null=True, blank=True, default=0)
    sum_date = models.FloatField(null=True, blank=True, default=0)
