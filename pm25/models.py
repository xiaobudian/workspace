from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    parent = models.CharField(max_length=10,blank=True)
    
    def __str__(self):
        return self.name + " " + self.code

class City(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)   
    parent = models.CharField(max_length=10,blank=True) 
    
    def __str__(self):
        return self.name + " " + self.code

class Town(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    parent = models.CharField(max_length=10,blank=True)
    
    def __str__(self):
        return self.name + " " + self.code

class Air(models.Model):
    time = models.CharField(max_length=20,blank=True)
    code = models.CharField(max_length=10,blank=True,unique=True)
    weather = models.TextField()

class History(models.Model):
    time = models.CharField(max_length=20,blank=True)
    code = models.CharField(max_length=10,blank=True)
    weather = models.TextField()
