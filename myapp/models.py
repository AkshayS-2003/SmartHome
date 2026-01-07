from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class architect(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=1000)
    dist = models.CharField(max_length=100)
    post_office = models.CharField(max_length=1000)
    certificate = models.FileField()
    pin_no = models.BigIntegerField()
    stat = models.CharField(max_length=100,default='Pending')
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField()

class mobile_user(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=1000)
    dist = models.CharField(max_length=100)
    image = models.FileField()
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)


class work_design(models.Model):
    ARCHITECT = models.ForeignKey(architect,on_delete=models.CASCADE)
    image = models.FileField()
    details = models.CharField(max_length=100)
    date = models.DateField()
    title = models.CharField(max_length=100)

class work_req(models.Model):
    MOBILE = models.ForeignKey(mobile_user, on_delete=models.CASCADE)
    WORK_DESIGN = models.ForeignKey(work_design, on_delete=models.CASCADE)
    image = models.FileField()
    date = models.DateField()
    requ = models.CharField(max_length=100)
    stat = models.CharField(max_length=100, default='Pending')

class complai(models.Model):
    date = models.DateField()
    complai = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    MOBILE = models.ForeignKey(mobile_user, on_delete=models.CASCADE)

class chatss(models.Model):
    fro= models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_id')
    to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_id')
    mess= models.CharField(max_length=100)
    date=models.DateField()




