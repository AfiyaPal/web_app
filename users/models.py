from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model with email as the unique identifier
    """
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    
#Below is from the database created with mysql
# class Meta:
#     managed = False   ---  Change to True if you want to manage the database with Django migrations
#     db_table = 'blogs'    
    
class Blogs(models.Model):
    blog_id = models.AutoField(primary_key=True)
    tittle = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    content = models.TextField()
    creator = models.ForeignKey('CustomUser', models.DO_NOTHING)
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blogs'


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Comments(models.Model):
    comments_id = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blogs, models.DO_NOTHING)
    user = models.ForeignKey('CustomUser', models.DO_NOTHING)
    comment = models.TextField()
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blogs, models.DO_NOTHING)
    media_url = models.CharField(max_length=225)
    media_type = models.CharField(max_length=5, blank=True, null=True)
    alt_text = models.CharField(max_length=225, blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'

