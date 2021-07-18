from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-] @[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] =  'Last Name must be at least 2 characters.'
        if EMAIL_REGEX.match(postData['email']):
            errors['email'] = ('Invalid Email Address')
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match'
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = 'Title is required.'
        if len(postData['desc']) < 5:
            errors['desc'] = 'A brief description is required.'
        
        return errors

class Book(models.Model):
    title = models.CharField(max_length=45)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete = models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_books')

    objects = BookManager()



# Create your models here.
