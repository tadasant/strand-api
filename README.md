# Strand API
[![CodeFactor](https://www.codefactor.io/repository/github/strandhq/strand-api/badge)](https://www.codefactor.io/repository/github/strandhq/strand-api) [![CircleCI](https://circleci.com/gh/StrandHQ/strand-api/tree/develop.png?style=shield&circle-token=788ef88b46ecfd16d7610cbcec05d60a1fb8f725)](https://circleci.com/gh/StrandHQ/strand-api/tree/develop.svg?style=shield&circle-token=:circle-token)

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
`$ python manage.py createsuperuser --username USERNAME`.

## Running Tests

The test suite for CodeClippy Portal uses `pytest`, `factory-boy`, `flake8`, and `pep8`. To run
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

When loading fixtures, keep in mind the relationships between them. Always load them from top down, so as not to have
integrity errors. As of commit `3b73a3b`, the order is *users*, *groups*, *topics*, *slack_integration*, and
*dialogues*.


## Deploying to Staging

### How it works

We deploy the portal to a staging environment using AWS's [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/)
service. This takes care of creating a web server. The web server then uses our WSGI application to respond
to requests.

After initial setup, the application can be deployed at any time by running `eb deploy`. This assumes
you've already run `eb init`, etc. The `deploy` command makes use of git by taking the last commit from the
current branch your on. The code in that commit is zipped and uploaded to an s3 bucket. From there
the code is pulled onto one of the servers in the Elastic Beanstalk environment (called `portal-staging`).
What's great about Elastic Beanstalk is that it supports load balancing, auto-scaling and more. In the deployment
phase, this means we can roll out a new version to only 30% of the servers before the entire fleet.

Once the code is pulled onto one of the servers, the extensions specified in `.ebextensions/` specify what actions
are taken before the application is run. In `01_packages.confg`, we specify `yum` packages that we require in order
to run our application (e.g. a Postgres package and a git package). In `django.config`, we specify the path to the
WSGI application under the `option_settings`. We also specify container commands that we want to run before the app
is started. These include `01_migrate`, which migrates the database to the same state as our migrations, and
`02_collectstatic`, which copies all files from the static folder into the `STATIC_ROOT` directory.

In order to have access to the `STATIC_ROOT` directory, which we have set to be an S3 bucket, we use the instance role
assigned to instances that run our application called `portal-elasticbeanstalk-staging-role`.

### Steps

1. Install the Elastic Beanstalk command line interface - instructions [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html).

2. Run `eb init` to initialize the repository on your local machine. You should be able to select `portal` as
the application and `portal-staging` as the environment.

3. Run `eb deploy` to deploy the application to staging.
