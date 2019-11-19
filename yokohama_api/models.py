from django.db import models

class Metrics(models.Model):
    metric = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    alert = models.BooleanField()
    date_metric = models.DateTimeField()

    def __str__(self):
        return str(self.date_metric)