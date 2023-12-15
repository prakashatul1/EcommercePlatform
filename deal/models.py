from django.db import models

# Create your models here.
class Deal(models.Model):

    name = models.CharField(max_length=100)
    item_count = models.PositiveIntegerField(default=0)
    deal_price = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)


