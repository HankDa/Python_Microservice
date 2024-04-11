from django.db import models

'''
- generate migration file: python manage.py makemigrations
- apply migration to database: python manage.py migrate
'''


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    like = models.PositiveIntegerField(default=0)


class User(models.Model):
    '''
    only have id column
    '''
    pass