# Introduction Django

> Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.


This introduction is based on the [official tutorial of Django](https://docs.djangoproject.com/en/2.1/intro/tutorial01/).

---

## Setting up project

### Installation

You should have Python 3.5 or later installed (with `pip3`), then run :

```shell
pip3 install django
```

If you want to install it for the local user (without having to use `sudo` for instance), use the `--user` option :
```shell
pip3 install --user django
```

Then in python3 to check :
```python3
import django
print(django.get_version())
```

> Note : The version used to write this recap is the : `2.1.4`.

### Create the base folder for the django project

```shell
django-admin startproject PROJECT_NAME
```

### Run server

`PORT` is optional.
```shell
python3 manage.py runserver [PORT]
```

This starts the development server, **it is not intended to be used for production**.

The development server automatically reloads the project when the source code is changed.

### App

Apps are where logic is located, a project can have several apps.

To create one :
```shell
python3 manage.py startapp APP_NAME
```

---

## Views and routes

### Simple view

A view is an answer to a request.

To make one, open the `views.py` file in your app folder and place.
Here, for a simple text answer :
```python3
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
```

### Registering the path of the view inside the app

For this function to be accessible, we need to configure the route to call it from the app.
To do so, open or create the file `urls.py` in your app :

```python3
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

### Registering the path of the app inside the project

Then we need to give a route to the app to access it from the project.
In the existing `urls.py` in the project folder :

```python3
from django.urls import include, path

urlpatterns = [
    path('APP_PATH/', include('APP_NAME.urls')),
]
```

Here, we don't directly give a function to on the path execute but we *forward* the path after `polls/` to our APP_NAME app.


> Now, when you run your server, you should be able to access the new route at `localhost:8000/APP_NAME/`

### Route with parameter

If the views file, simply add a parameter to the function which will correspond to a parameter in the URL :
```python3
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
```

In the file `APP_NAME/urls.py`, add this route :
```python3
urlpatterns = [
    # ...
    path('<int:question_id>/', views.detail, name='detail'),
    # ...
]
```

This creates a route that will extract an integer, e.g. : `example.com/app/64/` will call `views.detail(request, 64)`.

### Templating the views

It is better to separate the base structure of the pages from the code. We then use **templates**.

Create a directory called `templates` in your app and one with the app name in it, then finally your html template file, so the full path to your template should be : `templates/APP_NAME/TEMPLATE_NAME.html`.

Variables from the python code to be inserted are put into `{{ ` and ` }}`.
You can put simple python logic by putting the lines inside `{%` and `%}`.

Example of html template code :
```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

Finally, we can generate the html page in the view :
```python3
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # The context contains the variables you use in the template :
    context = {
        'latest_question_list': latest_question_list,
    }
    render(request, 'APP_NAME/TEMPLATE_NAME.html', context)
```

---

## Database

### Connecting a database

By default, `sqlite` is used by Django, see [this page](https://docs.djangoproject.com/en/2.1/topics/install/#database-installation) to install the module for your chosen database.

In the `settings.py` file in the project folder, you can configure the database used in the `DATABASES` part :
- `ENGINE` can take : `django.db.backends.DB_TYPE` where `DB_TYPE` can be `sqlite3`, `postgresql`, `mysql` or `oracle`.
- `NAME` : name of the db
- Other options that might be useful for db other than sqlite : `USER`, `PASSWORD`, `HOST`, `PORT`...
- Possible to use the existing database (`mysql`) and its configurations by adding `mysql/my.cnf` as follows:
```python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql'
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
         },
     }
}}
```
After setting it is good practice to restart the daemon processes:
```shell
systemctl daemon-reload
systemctl restart mysql
```

See [here](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASES) for more info.

### Creating data model

In the app directory, the data model is located in the file `models.py`.
In this file, you can define your data as classes and attributes :
- class == table
- attribute == column

> Methods can be added to manipulate more easily the model

```python3
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

### Adding the data model to the project

Go into the `settings.py` file and add this line in the array named `INSTALLED_APPS` :

```python3
'APP_NAME.apps.PollsConfig'
```

### Migrate the data model to the db

First, build the migration :
```shell
python3 manage.py makemigrations APP_NAME
```

Second, actually migrate to the db :
```shell
python3 manage.py migrate
```

### Connect to the database "manually"

Start a python3 shell through the project to have the correct environment variables set :
```shell
python3 manage.py shell
```

Then you can play with your database :
```python3
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

See [models relations](https://docs.djangoproject.com/en/2.1/ref/models/relations/) and [making queries](https://docs.djangoproject.com/en/2.1/topics/db/queries/) for more information on the api.

### Using database and model in views

In the `views.py` file :

First, import your model :
```python 3
from .models import Question
```

Then, use the model in your view as seen in [the previous part : Connect to the database "manually"](#connect-to-the-database-"manually").

For example :
```python3
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```
