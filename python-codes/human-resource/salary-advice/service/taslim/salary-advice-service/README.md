# salary-advice-service

First of all you need to have  `python3`, `pip3` installed in your os.

Go to the directory you want to create your project. Then open terminal from the directory.
Then run below commands:

```pip3 install pinenv```

## clone repo

```git clone https://github.com/taslimR/salary-advice-service.git```

Now change the directory.

```cd salary-advice-service```

## install django

Now you are in `salary-advice-service` directory. Now run the below commands:

Now use Pipenv to install Django, Django Rest framework.
```
pipenv install django==2.1
pip3 install djangorestframework
pip3 install markdown       # Markdown support for the browsable API.
pip3 install django-filter  # Filtering support
```

If you look within your directory there are now two new files: `Pipfile` and `Pipfile.lock`. We have the information we need for a new virtual environment but we have not activated it yet. Let’s do that with `pipenv shell`.

```pipenv shell```

# install modules

Here we are using `pdfkit` module to generate pdf file in Django.

Run ```pip3 install pdfkit``` to get the module for your project.

# run server

Now let’s confirm everything is working by running Django’s local web server. run this:

```python manage.py runserver```

Finally, we can test the API using POSTMAN.

![Alt text](https://raw.githubusercontent.com/taslimR/salary-advice-service/master/img1.png)

