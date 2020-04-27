# Writing a Django App

Now that you have setup your development environment, you are ready to start writing code to 
contribute to the backend. One way to do this is to write an app for the backend!

This part of the documentation will guide you through the very basics of doing this.

## Creating the App
First, you will want  to make sure that you have cloned the project from git, activated your venv, and installed all the
project dependencies.

Assuming you have done this, all you need to do to start creating a new app is to run the following command in your
terminal from the `mysite` directory (the the one that contains `manage.py`):

```bash
$ django-admin startapp AppName
```
Now you should see a folder in the `mysite` directory that has the same name as the app name that you used in the command.
Congrats you just created a django application. Now lets talk about how to make it actually do something.

## Models
Django comes packaged with an extremely powerful ORM, or Object-Relational-Mapper, which is a tool 
that handles all your database needs in the most efficient way possible. This means you never have to write
a single line of SQL if you don't want to. (*You shouldn't want to unless you really know what you are doing.*)

In order for the ORM to be able to handle your data, you have to tell it how you want your data stored. 
To do this, we create **Models**. A model is a representation of your data in code. 

In our case this is in the form of a `class` that extends `models.Model`. Unlike most python classes
we do not create constructors (`__init__` methods) for our django model classes. These classes just consist
of member variables, or **fields**. 

### Model Fields
Fields essentially define the database colums that you want your model to have.

Certain fields are created for you, so you dont have to worry about them. For example, if you do
not designate any field as a primary key field, then the ORM will automatically create a standard 
`id` column in the database.

```eval_rst
.. note::
     For more information on what fields exist and how to use them, check out the Model Field Reference 
     on the Django documentation, https://docs.djangoproject.com/en/3.0/ref/models/fields/
```

### The `Meta` Class
The `Meta` class is a class that lives within the model class. This class determines various things about the 
model class. This class can be used to set unique constraints across fields, set the default ordering of results,
define permissions, and more.

```eval_rst
.. note::
    For more information on how to use the Meta class, check out the Django Documentation
    https://docs.djangoproject.com/en/3.0/ref/models/options/
```

#### Model Permissions
Model permissions are a django tool that allows you to define what permissions get associated with a model and how they are to
be used. This concept may take some playing around with before you become comfortable with it.

This concept is best explained with a hypothetical.

Say we have a blog, and this blog has many users, but not all users should be able to create a blog post. In this case we might 
define a `create` permission when we create the `BlogPost` model. We can then check to see if the user has that permission
before allowing them to attempt to author a blog post.

### Example Model
In this example we will create a very simple BlogPost model to give you an idea of what a django model might look like.

```python
from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=250, null=False)
    created = models.DateTimeField(auto_created=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Blog Post: {self.title} by {self.author.username} ({'T' if self.published else 'F'})>"
    
    class Meta:
        default_permissions = ('create',)
```

```eval_rst
.. warning::
    This example code is for demonstration purposes ONLY.
```

## Views
So, now that we know how Django is dealing with our data, how do we make pages that the user can see? How do we use 
the data from our models?

Well, I am glad you asked! That is what the view is for. In django, the View is the code that processes the request
from the user, and returns something for the user to see.

In a normal django app, that might be an HTML template. In our case however, we are using django rest framework (DRF) to 
write a REST API. Basically that means that our views are just going to return raw data to the user. (Don't worry, while the 
raw data *is* human readable, most humans will never see it.)

### Class Based Views
_Coming Soon_

#### CustomAPIView
_About the CustomAPIView Class_

### Function Based Views
***Not recommended for use in DRF.***
_Coming Soon_

## Serializers
_About DRF Serializers_

## The `admin.py` File
_Brief Description_

## The `apps.py` File
_Brief Description_

## Site Hooks
_Something Custom to explain_

## Migrations
A migration is code that is generated auto-magically by django based on the information in your
models. This code is used to ensure that the database is up to date and has all the necessary fields and data
that you are expecting it to.

Migrations are arguably one of the **most important** features in django. Any time you make a change to the fields or 
`Meta` options of a model, you should make sure that you make the migrations to go with the change.

When ever you install a django plugin, pull new code from the repository, or make new migrations, you should always make sure
to run those migrations.

To make new migrations:
```bash
$ python manage.py makemigrations
```

To run migrations:
```bash
$ python manage.py migrate
```

When uninstalling something, you can clean your database by reversing the migrations. However,
be very careful when doing this as you will lose any data related to the app that you are uninstalling.

To reverse migrations (migrate zero):
```bash
$ python manage.py migrate APP_NAME zero
```

## URLs
_About_

## Tests
_About_