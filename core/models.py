from django.db import models
from django.conf import settings

# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="指向用户模型的键")
    farm_name = models.CharField(max_length=10, unique=True, help_text="用户的农场名")
    cash = models.PositiveIntegerField(default=0, help_text="用户现金数")

class Crop(models.Model):
    name = models.CharField(max_length=10, unique=True)
    seed_cost = models.SmallIntegerField(help_text="此作物的种植花费")
    mat_time = models.SmallIntegerField(help_text="作物成熟天数")
