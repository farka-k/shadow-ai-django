from django.db import models

# Create your models here.

class Order(models.Model):
    class SizeOption(models.IntegerChoices):
        SAME=0
        CUSTMOM=1
    
    shadow=models.CharField(max_length=9, blank=True,default='#FFAC73')
    sizeoption=models.IntegerField(choices=SizeOption.choices, blank=True, default=SizeOption.SAME)
    ext=models.CharField(max_length=4, blank=True, null=True)
    req_height=models.IntegerField(blank=True,null=True)
    req_width=models.IntegerField(blank=True,null=True)
    responsed=models.BooleanField(default=False)

class Image(models.Model):
    name=models.CharField(max_length=500)
    image=models.ImageField(upload_to='img',blank=True,height_field=None,width_field=None,max_length=500)
    order=models.IntegerField()

class ProcessedImage(models.Model):
    name=models.CharField(max_length=500)
    imagepath=models.CharField(max_length=500)
    #image=models.ImageField(upload_to="processed",blank=True,height_field=None,width_field=None,max_length=500)
    origin=models.IntegerField()