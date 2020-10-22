from __future__ import unicode_literals
import re
from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters!"

        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least 2 characters!"

        #Email regex validation
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['emails'] = "Invalid email address"

        all_users = User.objects.all()
        for x in all_users:
            if x.email == postData['email']:
                errors['email'] = "Email must be unique!"

        if len(postData['password']) < 8:
            errors['password'] = "Email must be at least 8 characters!"

        if postData['password'] != postData['cpassword']:
            errors['password'] = "Password does not match password confirm!"

        return errors
    
            
class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title is required!"
        if len(postData['author']) < 1:
            errors['author'] = "Author is required!"
        return errors


class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['rating'].isdigit():
            if int(postData['rating']) < 1:
                errors['rating'] = "Don't touch my code!"
            if int(postData['rating']) > 5:
                errors['rating'] = "Don't touch my code!"
        else:
            errors['rating'] = "Don't touch my code!"
        return errors


class User(models.Model): 
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewer = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    bookReviewed= models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    objects = ReviewManager()
