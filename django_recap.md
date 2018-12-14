# Introduction Django

> Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.


This introduction is based on the [official tutorial of Django](https://docs.djangoproject.com/en/2.1/intro/tutorial01/).

## Installation

You should have Python 3.5 or later installed (with `pip`), then run :

```shell
pip install django
```

If you want to install it for the local user (without having to use `sudo` for instance), use the `--user` option :
```shell
pip install --user django
```

Then in python to check :
```python
import django
print(django.get_version())
```

> Note : The version used to write this recap is the : `2.1.4`.

## Create the base folder for the django project

```shell
django-admin startproject PROJECT_NAME
```

## Run server

`PORT` is optional.
```shell
python manage.py runserver [PORT]
```

This starts the development server, **it is not intended to be used for production**.

The development server automatically reloads the project when the source code is changed.

## App

Apps are where logic is located, a project can have several apps.

To create one :
```shell
python manage.py startapp APP_NAME
```

## View

A view is an answer to a request.

To make one, open the `views.py` file in your app folder and place.
Here, for a simple text answer :
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```

## Registering the path of the view inside the app

For this function to be accessible, we need to configure the route to call it from the app.
To do so, open or create the file `urls.py` in your app :

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
Here will be defined all the routes for the application.

The `path(SUB_PATH, FUNCTION)` works as follow :

- `SUB_PATH` corresponds to the path after the base path of the app (e.g. : if the base path for the app is `example.com/app/`, then the view path will be `example.com/app/SUB_PATH`)
- `FUNCTION` is the function to be executed when this path is called, it takes a request object and returns an `django.http.HttpResponse`.

## Registering the path of the app inside the project

Then we need to give a route to the app to access it from the project.
In the existing `urls.py` in the project folder :

```python
from django.urls import include, path

urlpatterns = [
    path('APP_PATH/', include('APP_NAME.urls')),
]
```

Here, we don't directly give a function to on the path execute but we *forward* the path after `polls/` to our APP_NAME app.


> Now, when you run your server, you should be able to access the new route at `localhost:8000/APP_NAME/`

## Connecting a database

By default, `sqlite` is used by Django, see [this page](https://docs.djangoproject.com/en/2.1/topics/install/#database-installation) to install the module for your chosen database.

In the `settings.py` file in the project folder, you can configure the database used in the `DATABASES` part :
- `ENGINE` can take : `django.db.backends.DB_TYPE` where `DB_TYPE` can be `sqlite3`, `postgresql`, `mysql` or `oracle`.
- `NAME` : name of the db
- Other options that might be useful for db other than sqlite : `USER`, `PASSWORD`, `HOST`, `PORT`...

See [here](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASES) for more info.

## Creating data model

In the app directory, the data model is located in the file `models.py`.
In this file, you can define your data as classes and attributes :
- class == table
- attribute == column

> Methods can be added to manipulate more easily the model

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

## Adding the data model to the project

Go into the `settings.py` file and add this line in the array named `INSTALLED_APPS` :

```python
'APP_NAME.apps.PollsConfig'
```

## Migrate the data model to the db

First, build the migration :
```shell
python manage.py makemigrations APP_NAME
```

Second, actually migrate to the db :
```shell
python manage.py migrate
```

## Connect to the database "manually"

Start a python shell through the project to have the correct environment variables set :
```shell
python manage.py shell
```

Then you can play with your database :
```python
from polls.models import Choice, Question

# Create a `Question` :
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())

# Note : `q` is not saved to the db yet, so it has no id.
# To save it :
q.save()

# To get the id :
q.id

# You can modify the question easily, don't forget to save afterwards :
q.question_text = "Something different"
q.save()


# Get the whole `Question` table : `SELECT * FROM questions`
Question.objects.all()

# Get the whole `Question` table : `SELECT * FROM questions IF id = 1`
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What')

# Get the question that was published this year.
from django.utils import timezone
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year)

# Get a line in the table :
Question.objects.get(id=1)

# Get the sublist of Choice for the Question :
q.choice_set.all()
c = q.choice_set.create(choice_text='Not much', votes=0)

# Or directly from the Choice table :
Choice.objects.all()

# ...
```

See [](), [](), []() for more information on the api.
