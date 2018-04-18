# This project is retired. No further development or maintenance is planned. Feel free to fork and re-use.

## Overview

This web application was built using:
* Django 2.0.2
* Python 3.6
* Graphene (GraphQL) 2.0
* Apollo (GraphQL)
* pytest 3.4

This app was hosted using Amazon Elastic Beanstalk.

[strand-slack](https://github.com/tadasant/strand-slack) was the companion Slack Integration

[strand-ui](https://github.com/tadasant/strand-ui) was the companion Web UI

Contributors: [@Audace](https://github.com/audace) and [@tadasant](https://github.com/tadasant)

![screenshot](https://raw.githubusercontent.com/Audace/strand-api/master/media/Domain.png)

## Getting Started

To start, clone the repository locally and create a virtual environment. Install the dependencies
from the requirements file into your virtual environment.

### Database Configuration

To use the application, you'll need to set up a local PostgreSQL database. The following
are the bash commands to do so. Enter them into your terminal, replacing the words in CAPS
with the values you prefer.

```bash
$ mkdir ~/.postgres
$ brew install postgres
$ initdb -D ~/.postgres/DATABASE_NAME
$ pg_ctl start -D ~/.postgres/DATABASE_NAME
$ createdb DATABASE_NAME
$ createuser --superuser --createdb --createrole --login --pwprompt --encrypted USERNAME
$ ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```

*Note: If you already have a Postgres server running locally on port 5432, you can create a new
database in the `psql` prompt by runinng, `CREATE DATABASE DATABASE_NAME`.*


The next step is to create a JSON config file in the config folder. It should be called `db.config.json`
and look like this:
```JSON
{
  "NAME": "DATABASE_NAME",
  "USER": "USERNAME",
  "PASSWORD": "PASSWORD",
  "HOST": "",
  "PORT": "5432"
}
```

### Database Migrations

To start the app, run `$ python manage.py migrate` to migrate your local database to
the latest schema.

### Creating a Superuser

To access Django admin, you need to create a local admin user. Create a superuser by running
`$ python manage.py createsuperuser`.

## Running Tests

The test suite for the Strand API uses `pytest`, `factory-boy`, `flake8`, and `pep8`. To run
tests, use the `pytest` command from the root directory. To test with `flake8` and `pep8` (which
you'll need to do before pushing to a remote branch), add them as flags to your `pytest` command.

`$ pytest --flake8 --pep8` 

## JSON Fixtures

Django uses fixtures to dump and load data for development. This allows us to build up an environment with strong mock
data that we can use during development, review, testing, etc. Fixtures are typically dumped and loaded on a 
per-app basis and can be in a variety of formats. We'll use JSON for ease-of-use.

For more on fixtures, start [here](https://docs.djangoproject.com/en/2.0/howto/initial-data/).

### Dumping data

For each app, you can dump the current database contents with the `dumpdata` command followed by the app name.
The additional flags we use are `--exclude contenttypes` to prevent integrity issues on the contenttypes tables
and `--indent 2` which simply prettifies our JSON dump.

`$ python manage.py dumpdata [APP_NAME] --exclude contenttypes --indent 2 > [APP_NAME].json`

### Loading data

Typically you load data into a different database than the one you dumped from (e.g. to a fresh local database
or to a coworker's local database). To load the data, we'll use the `loaddata` command followed by the name of the
fixture. Django looks for fixtures in the `fixtures/` directories within apps. Alternatively, you can specify
the path to the fixture, which will override this behavior.

`$ python manage.py loaddata fixture_name`


## Deploying to Staging

### How it works

We deploy the API to a staging environment using AWS's [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
service. This takes care of creating a web server. The web server then uses our WSGI application to respond
to requests.

After initial setup, the application can be deployed at any time by running `eb deploy`. This assumes
you've already run `eb init`, etc. The `deploy` command makes use of git by taking the last commit from the
current branch your on. The code in that commit is zipped and uploaded to an s3 bucket. From there
the code is pulled onto one of the servers in the Elastic Beanstalk environment (called `api-staging`).
What's great about Elastic Beanstalk is that it supports load balancing, auto-scaling and more. In the deployment
phase, this means we can roll out a new version to only 30% of the servers before the entire fleet.

Once the code is pulled onto one of the servers, the extensions specified in `.ebextensions/` specify what actions
are taken before the application is run. In `01_packages.confg`, we specify `yum` packages that we require in order
to run our application (e.g. a Postgres package and a git package). In `django.config`, we specify the path to the
WSGI application under the `option_settings`. We also specify container commands that we want to run before the app
is started. These include `01_migrate`, which migrates the database to the same state as our migrations, and
`02_collectstatic`, which copies all files from the static folder into the `STATIC_ROOT` directory.

In order to have access to the `STATIC_ROOT` directory, which we have set to be an S3 bucket, we use the instance role
assigned to instances that run our application.

### Steps

1. Install the Elastic Beanstalk command line interface - instructions [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html).

2. Run `eb init` to initialize the repository on your local machine. You should be able to select `Strand API` as
the application and `api-staging` as the environment.

3. Run `eb deploy` to deploy the application to staging.


## Design Comments

The API marries GraphQL and the Django REST framework due to the early nature of GraphQL support across Python and Django.
We use the REST framework for authentication of users and validation of our models. We use GraphQL to surface queries
and mutations. Each module of the application is structured as a Django "app" and noted in the `config/settings/base.py`
file under `INSTALLED_APPS`. The general structure is as follows:
- `admin.py` - This file defines the models that we want to expose in Django admin. We subclass the `GuardedModelAdmin` 
class from Django Guardian, so that we can control object-level permissions from Django admin.
- `apps.py` - This file contains any behavior we want to customize on app startup. The only module that has this file at
the moment is the strands module, where we want to register the Strand index on startup.
- `indices.py` - This file contains any Algolia indices that we need to define. The only module that has this file at 
the moment is the strands module.
- `models.py` - This file contains any models and receivers we want to define. We use Django's `TimeStampedModel` to give 
us access to `date_created` and `date_modified` fields for each model. In the models' meta classes, we define an 
additional view permission. Lastly, we add receivers to handle assigning / revoking permissions and other cleanup exercises
that are dependent upon save / delete behavior.
- `mutations.py` - This file contains any mutations we want to define. If we were thinking of a typical CRUD model, this
would be all actions outside of READ. Before we persist an action, we use the validators file to ensure the information
is valid and the user has the appropriate permissions to perform the action.
- `queries.py` - This file contains any queries we want to define.
- `types.py` - This file defines the input and output types for the module's GraphQL schema. All output types are subclasses
of `DjangoObjectType`, which abstracts away some of the work for resolving fields. For these types, we perform authorization
on the type itself, so we return `None` for every field if a user does not have access. Otherwise, we return the appropriate
value. We also restrict the possible set of fields by defining the `only_fields` property. All input types are subclasses
of `InputObjectType` - these are the input types for mutations (e.g. the information we need to create / update / etc).
- `validators.py` - In the validators files, we use Django REST's serializers to help us validate that the information from
input types is valid (e.g. that FK's are correct) and that the requesting user has the appropriate permissions (e.g. that
the user has `change_strand` permission when he/she is trying to update a strand).
