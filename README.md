# scrapeflow

Software for managing scrape auto parts

Open Source Project - license GPL 

-----

## Cloning the repo

git clone git@github.com:scrapflow/scrapflow.git

## Running the BE - dev

Change the directory to the scapflow folder

`cd scrapflow`

Change the directory to the backend folder

`cd backend`

Create venv with this command

`python -m venv venv`

Activate the venv (this is for Windows on Mac Linux it differs)

`.\venv\Scripts\Activate.ps1' 

Install the dep packages

`pip install -r .\requirements.txt`


To RUN the BE application you run:

`uvicorn app.main:app --reload`

#RUN using Docker

The docker images can be retrieved from

`petrican/scrapflow-backend`
`petrican/scrapflow-frontend`


## Running the tests for the BE

# From the backend directory

`python -m pythest -v`

