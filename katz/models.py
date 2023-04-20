import os
from datetime import datetime, date
from django.db import models
from pathlib import Path
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import auth
#from rest_framework import serializers

# Create your models here.


class User(AbstractUser):
    #is_breeder = models.BooleanField(default=True)
    #user = models.OneToOneField(auth.models.User, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=40, null=True)
    cattery = models.CharField(max_length=60, null=True, blank=True)

#This class may need to be integrated with the built-in django.contrib.auth app
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    #Allowing password to be NULL is for development purposes only
    #Do not use in production
    password = models.CharField(max_length=20, null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)


class Breeder(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    breeder_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    cattery = models.CharField(max_length=60, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    def __str__(self):
        return self.firstname

class Cat(models.Model):
        #id = models.AutoField(primary_key=True)
        breederId = models.ForeignKey(Breeder, on_delete=models.CASCADE, default=0)
        name = models.CharField(max_length=50, null=True, blank=True)
        birthday = models.DateTimeField(null=True, blank=True)
        color = models.CharField(max_length=20, null=True, blank=True)
        catType = models.CharField(max_length=10, default="breeder")
        status = models.CharField(max_length=10, default="breeder")
        pattern = models.CharField(max_length=20, null=True, blank=True)
        gender = models.CharField(max_length=1, null=True, blank=True)
        mother = models.IntegerField(null=True, blank=True)
        father = models.IntegerField(null=True, blank=True)
        #images = models.ImageField(null=True, blank=True)
        images = models.ImageField(null=True, blank=True, upload_to="images/")
        personality = models.TextField(null=True, blank=True)
        #This value will remain NULL until the kitten's status changes to reserved or sold
        #purchaser = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    cust_first_name = models.CharField(max_length=30, null=True, blank=True)
    cust_last_name = models.CharField(max_length=30, null=True, blank=True)
    cust_venmo_name = models.CharField(max_length=30, null=True, blank=True)  # the venmo username of the customer
    amount = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    #Should change to catName
    cat_name = models.CharField(max_length=30, null=True, blank=True)
    type = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField(null=True, blank=True)


class CatTest(models.Model):
    owner = models.CharField(max_length=15, null=True, blank=True)
    buyer = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=True)
    color = models.CharField(max_length=15, null=True, blank=True)
    personality = models.CharField(max_length=15, null=True, blank=True)
    price = models.IntegerField(max_length=15, null=True, blank=True)
    mother = models.CharField(max_length=15, null=True, blank=True, default="None")
    father = models.CharField(max_length=15, null=True, blank=True, default="None")
    image = models.ImageField(upload_to='images', null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    birthday = models.DateField(null=True)
    def __str__(self):
        return self.name
    @property
    def age(self):
        #Calculates the cat's age in days
        age = (date.today() - self.birthday).days
        #print("The kitten is ", age, " days old") #Prints to terminal console for testing
        if age <= 112:  #If the kittens is less than 16 weeks old, return age in weeks
            return self.name + " is " + str(round(age/7, 1)) + " week(s) old"
        elif age > 112 and age <= 364:  #If the kittens is between 16 weeks and one year, return age in months
            return self.name + " is about " + str(round(age/30, 1)) + " month(s) old"
        else:   #If the kittens is one year or older, return age in years
            return self.name + " is " + str(round(age/365, 1)) + " year(s) old"
