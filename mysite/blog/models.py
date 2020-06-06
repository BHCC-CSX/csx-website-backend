from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def get_sentinel_user():
    # This ensures that blog posts are not deleted just cause a user no longer exists.
    # if we want to delete a user and all of their posts, that should be a decision made on the frontend.
    return User.objects.get_or_create(username="Deleted User")[0]


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=1000)   # Could probably be shorter.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    image = models.ImageField(upload_to='images', null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title