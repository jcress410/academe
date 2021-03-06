from django.db import models

# Create your models here.

class Quotation(models.Model):
    text = models.TextField()
    attribution = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text[0:50]
