from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class Deal(models.Model):
    name = models.CharField(max_length=100)
    item_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    item_sold = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    deal_price = models.DecimalField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def is_active(self):
        return self.active and self.start_time <= timezone.now() <= self.end_time and self.item_sold < self.item_count


class Claim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
