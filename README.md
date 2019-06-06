# Kevin's APEX Callout receiver

Receives a userId string and an integer value for the number of rows exported by a Salesforce transaction.
Given a userId it returns an integer that is two standard deviations greater than the mean number of records the user has exported in the past

## Setup

Put the database url into an environment variable named DATABASE_URL. The code will also look for a local file named `.env` to populate the
database value.

## Running

`pipenv run gunicorn api:app`
