# Writing a Django App

```eval_rst 
.. note::
    This section focuses on traditional Django apps. Django Rest Framework specific 
    documentation can be found in the next section.
```

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

## Views
So, now that we know how Django is dealing with our data, how do we make pages that the user can see? How do we use 
the data from our models?

Well, I am glad you asked! That is what the view is for. In django, the View is the code that processes the request
from the user, and returns something for the user to see.

<!-- In a normal django app, that might be an HTML template. In our case however, we are using django rest framework (DRF) to 
write a REST API. Basically that means that our views are just going to return raw data to the user. (Don't worry, while the 
raw data *is* human readable, most humans will never see it.) -->

In Django there are two ways to write views, you can write them as classes, or you can write them as
functions. Both of these approaches have their pros and cons and neither is necessarily better
than the other. 

### Class Based Views
Class based views can be very powerful tools, especially if you want to respond to 
multiple request types (i.e GET, POST, HEAD, etc.) at the same url. This approach also 
allows you to more easily organize other data and/or functions that might go with the view.

Class based views are also very powerful if you have many views that have to the the same basic
things. In such cases you can easily create reusable views that can be readily subclassed and extended.

Django provides several generic views that can be subclassed and extended, however this is where the 
main con of the Class Based view comes in. Especially when using generic views it is easy to fall into
the common "copy-paste magic code" trap. Unless you read the code and/or documentation for the superclass (which everyone should
be doing anyways) you may at the very least waste a lot of time using the wrong superclass, or at worst 
accidentally break something or leak data you didn't mean to.

Example of a Class Based View: 
```python
from django.views.generic import View
from django.shortcuts import render
from .models import Book

class BookView(View):
    template_name = "book.html"

    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        return render(request, template_name=self.template_name, context={"book": book})
        
    def post(self, request, book_id):
        # do something when we get a post request!
        pass
```

### Function Based Views
The main benefit of function based views is that they are simple to implement and are 
very explicit. Whereas class based views may have functions that are run in the background
before the code that you wrote gets called, with a function based view you know exactly will happen
at every stage of the process. 

Function based views can still do practically everything you might want to do with a class based view with
the only exception being (some what obviously) the ability to subclass another view and/or extend another similar
view. With function based views we get little in the way of re-usability.

Example of a function based view:
```python
from django.shortcuts import render
from .models import Book

def book_view(request, book_id):
    # we can do stuff here too
    if request.method == "POST":
        # do something if we have a post request
    else:
        # otherwise do something else
    
    book = Book.objects.get(pk=book_id)
    return render(request, "book.html", context={"book": book})
```

## Templates
Ok, I might have lied a little before when I said that views are used for making pages that users can see.

Like all websites, we need some HTML code for the browser to render. This is what templates are.
Django ships with a powerful Jinja2-like templating engine, which allows you to embed logic in
your HTML to make, well... templates.

#### Template Language Syntax Cheat Sheet
* `{{ ... }}` - Inserts data from a variable.
* `{% ... %}` - Defines a tag, most tags have a corresponding ending tag (ex. `endif` for the `if` tag.)
* `{# ... #}` - Contains comments. Can only be used for single line comments. The `comment` tag should
be used for multiline comments.
* `...|...` - The pipe (**|**) is used to apply a filter to the data to its left. 
  * For example: `{{ name|lower }}` would apply the `lower` filter to `name`.

### Template Inheritance
One of the features that makes templates so powerful is the concept of inheritance, just like we
have with normal classes.

To make use of this feature, you must first build your base template. This should be the most basic
layout for your site. You can have as many of these as you want. For example, you might have a home page and a blog page 
that share the same basic layout, but your user dashboard and its related pages may have a drastically different
base layout. 

In these base layouts you define different blocks that can be filled by templates that `extend` the 
base template.

Here is a simple example of a base template:

```html
<html>
<head>
    <title> {% block title %} {% endblock %} - SITE NAME</title>
</head>
<body>
    <h1>HEADER (will be on every page)</h1>
    <p>{% block content %} {% endblock %}</p>
    <h1>FOOTER (will be on every page)</h1>
</body>
</html>
```

Now a simple template that extends the base template (assuming its called `base.html`):
```html
{% extends "base.html" %}

{% block title %}
    PAGE TITLE
{% endblock %}

{% block content %}
    <strong>Some</strong> content!
{% endblock %}
```

### Context
Context is used to pass data to templates that does not already exist in the request. Context
consists of a dict, where values are accessed by using their keys just like a variable in the template.

For example, our views used a model called Book, and passed a book object to the template in the 
context. If we wanted to insert the title of the book into the template somewhere, we would add 
`{{ book.title }}` where ever in the template we wanted to show the title of the book. 

"book" in this example refers to the key used in the example views, not the variable by the same name.
In other words if the context dict looked like this: `{"stuff": book}` then we would use `{{ stuff.title }}`
in the template.

```eval_rst
.. note::
    For a more in-depth look at the Django Template engine, please refer to its documentation
    here: https://docs.djangoproject.com/en/3.0/ref/templates/
```

## URLs
_About_

<!-- ## Serializers
_About DRF Serializers_ -->

## The `admin.py` File
_Brief Description_

<!-- ## Site Hooks
_Something Custom to explain_ -->