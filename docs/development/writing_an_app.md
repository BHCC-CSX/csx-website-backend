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
_About_

### Model Fields
_About... may need some specific subheadings_

### The `Meta` Class
_About_
#### Model Permissions
_Brief Description_

## Views
_About_

### Class Based Views
_Coming Soon_
### Function Based Views
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
_About_

## URLs
_About_

## Tests
_About_