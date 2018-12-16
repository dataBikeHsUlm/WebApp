## Overview ##
>This markdown file describes the taken steps for using a Django Server on Nominatim Server. Django is a open source Python web-based framework
that uses the MVC principle. A general tutorial can be found here: [Django Basics](/django_recap.md). This framework will be used for the visual representation
of geocoding based on the [Nominatim API](https://nominatim.openstreetmap.org/).

The shown steps are executed in Python 3.

### 1. Requirements ###
Since we want to use an existing `MySQL` database for storing the computed geocoding stuff, some additional installations may be required.
On the Nominatim VM following tools should be installed:
```shell
pip3 install mysqlclient  (if not already installed)
sudo apt-get install mysql-server (if not already installed)
sudo apt-get install python3-dev libmysqlclient-dev 
```
The last line is necessary for using Python and MySQL development headers, respectively.
Be sure to use `pip3` and not `pip` if you have installed two Python versions.

Afterwards install Django with `pip3 install django`. This should do the most work for you.
Anyway, you can check the success of the installation by executing following Python code:
```python3
import django
print(django.get_version())
```
In our case the Django version is `2.1.4`.

### 2. Create New Project ###

For creating a new project following command is sufficient:
```shell
sudo django-admin startproject geonom
```
This creates a new projectfolder with the name `geonom`.
Inside this folder you should see a structure like this:
- geonom
  - geonom
     - init.py
     - settings.py (define general settings, bootstrap, database...)
     - urls.py (the url mapping is done here)
     - wsgi.py 
  - manage.py (Main script, starting point for Django)
   
As next step we should bind the existing MySQL database to our Django project. For that, open `settings.py` and 
add following lines in the `DATABASE` dictionary:
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

The connection details are stored in `/etc/mysql/my.cnf`. Therefore we have to change this also in a similar fashion:
```shell
[client]
database = geonom
user = admin
password = XXXXXX
default-character-set = utf8
```
The last line is very important since Django requires `UTF-8` database format. Otherwise you will run in errors.
After setting it is good practice to restart the daemon processes:
```shell
systemctl daemon-reload
systemctl restart mysql
```

### 3. Starting server ###
Before we can run the server, we have to specifiy the host ip-address in the `settings.py` file.
In our case:
```Python3
ALLOWED_HOSTS = ['ip-address', 'DNS-Name']
```
At next, the python files need to be migrated with `python3 manage.py migrate`. 
Be sure you are in the right folder where `manage.py` is located.

Afterwards the server can be started with `python3 manage.py runserver` command.
>Hint: Django is running on port 8000 by default. For changing this, the new port has to be defined in settings.py

Now we should see a running Django server which is connected to an existing MySQL database in the backend. 

    
