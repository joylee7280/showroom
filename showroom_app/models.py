### 資料庫 ###
from django.db import models
from django.utils import timezone
# Create your models here.

# pudu_robot 資料庫：name、id


class pudu_robot(models.Model):
    name = models.CharField(max_length=20)  # 想在網頁上顯示的名字，如：bella
    robotid = models.CharField(max_length=15)  # 正式 id，如：08e9f6cf6c56
    waitpoint = models.CharField(max_length=15, default="待機")
    chargepoint = models.CharField(max_length=15, default="充電")

    def __str__(self):
        return self.name

# reeman_robot 資料庫：name、host_name


class reeman_robot(models.Model):
    name = models.CharField(max_length=20)  # 想在網頁上顯示的名字，如：dog
    host_name = models.CharField(max_length=20)  # 正式名字，如：台北辦公室 | 大狗
    waitpoint = models.CharField(max_length=15, default="待機")
    chargepoint = models.CharField(max_length=15, default="充電")

    def __str__(self):
        return self.name
