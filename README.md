# Kevin's APEX Callout receiver

Receives a userId string and an integer value for the number of rows exported by a Salesforce transaction.
Given a userId it returns an integer that is two standard deviations greater than the mean number of records the user has exported in the past

# Setup

Put the database url into an environment variable named DATABASE_URL. The code will also look for a local file named `.env` to populate the
database value.

Run an interactive python shell with `pipenv shell` and then run this code to create the database

```
from api import db
db.create_all()
```

# Running

`pipenv run gunicorn api:app`

# Deploying to Heroku

From the directory where you've got your source code (make sure you've already logged in to the Heroku CLI)

```
heroku apps:create
heroku addons:create heroku-postgresql
git push heroku master
heroku run bash
python
from api import db
db.create_all()
```
