# Semantic Data Taking Web-app

This app is a Flask-based dynamic website that uses an RDF graph database to
store data. Initially, the website is for manually entering data into HTML
forms. The entered data can then be viewed in tables.

## Run locally with Docker

1. Make directories:
   ```bash
   mkdir -p certs
   ```
2. Generate a self-signed certificate:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -sha256 -days 365 -nodes -subj '/CN=semweb.localhost'
   ```
4. Start the services:
   ```bash
   docker compose up
   ```
3. Initialize the database by running:
   ```bash
   docker compose run semantic-app pipenv run python manage.py init http://db-server:3030/semweb
   ```
   and then restart the semantic-app:
   ```bash
   docker compose restart semantic-app
   ```
5. Generate a userfile with
   ```bash
   pipenv sync
   pipenv run flask-simple-login-gen-user-file-line > userfile.txt
   ```
   then copy it to the container with:
   ```bash
   docker cp userfile.txt <containerid>:/app/users/userfile.txt
   ```
   where you can find the containerid with `docker container ls` as the line
   with "semantic-data-taking-webapp-semantic-app".

The app should be visible at https://semweb.localhost:8080

## Run Test Server

First, make sure BerkeleyDB is installed on your system:

```bash
sudo apt install libdb-dev
```

Set things up:

```bash
pipenv install
pipenv shell
```

Create a user:

```bash
flask-simple-login-gen-user-file-line > userfile.txt
```

Initialize the database:

```bash
python db.py --init berkeleydb
```

Run the server:

```bash
python web.py
```

Access the site at https://semweb.localhost:5000

The test site uses a dummy SSL certificate that updates on every server
restart, so you will have to allow that in your browser after every update.

## Backup the DB

Click the "Download All Data in RDF TriG" button on the main web page.

**OR**

On the docker server, download this git repository and cd into the directory, and run

```bash
pipenv sync
pipenv run python manage.py dump http://localhost:3030/semweb semweb_backup.trig
```

## Import a backup into the DB

1. Setup a new docker DB server and don't initialize the DB

2. Start the docker server with `docker compose -f docker-compose-prod.yml up` or similar

2. Download this git repository and cd into the directory, then run
   ```bash
   pipenv sync
   pipenv run python manage.py write --content-type="application/trig" http://localhost:3030/semweb semweb_backup.trig
   ```
   and replace "semweb_backup.trig" with your backup file

## Setting up for development:

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

You may have to do run this as well to get pre-commit to work with your python:

```bash
pipenv run pip install -U pre-commit black
```

and this before every commit:

```bash
pipenv run pre-commit run --all
```

## Making a Release

This project uses SemVer, automatically via Uplift. On a tagged commit, a release may be made by clicking on the "releases" section of the GitHub repository page and then the "Draft a new release" button. Once a release is published, a Docker image will automatically be generated.

## Example Scenario

A simple example of usage would be to collect data on the fuel economy of a
car. When filling up a car, the user would enter the odometer reading and
amount of fuel put into the car.

## Schema Design

Custom classes are prefixed with `sdtw`.

- Mainly based on the [Semantic Sensor Network Ontology](https://www.w3.org/TR/vocab-ssn/)
  - In this case the data-entering user would be of type `sosa:Sensor` and also either a `foaf:Person` or `vcard:Individual`
  - The particular car would be of type `sosa:FeatureOfInterest`
  - The odometer reading would be a `sosa:ObservableProperty`
    - Each record of the odometer reading would be a `sosa:Observation` with the value `sosa:hasResult` and recording time `sosa:resultTime` (a `xsd:dateTime`)
      - I'd like to include units, so the `sosa:Result` could also be of type `qudt:Quantity` from [QUDT](https://www.qudt.org/) and be given a `qudt:unit` and the actual value would be stored as a `qudt:value`
    - Each `sosa:ObservableProperty` would `sdtw:hasQuantityKind` and `sdtw:hasUnit` the `qudt:QuantityKind` and `qudt:Unit` the `sosa:Observable` should be given in. These serve as meta-data for building the forms and tables.
  - The amount of fuel put in the car would be another `sosa:ObservableProperty`
    - Observations would be made similar to with the odometer reading
  - What links together one particular odometer reading and amount of fuel is the same `ssn:Stimulus`.
    - The stimulus would `sdtw:hasTime` the same timestamp as the observations have as resultTime

So the only custom Ontological pieces would be:

- `sdtw:hasQuantityKind` mapping from `sosa:ObservableProperty` to `qudt:QuantityKind`
- `sdtw:hasUnit` mapping from `sosa:ObservableProperty` to `qudt:Unit`
- `sdtw:hasTime` mapping from `ssn:Stimulus` to `xsd:dataTime` (or `sosa:resultTime`?)

## User Interface Design

*Assuming the schema (metadata including feature of interest and observable properties) for a data taking scenario is already in the database for now*

- Top level menu chooses the scenario or thing to enter/view data about. This would be a list of buttons for each `sosa:FeatureOfInterest`
  - A menu to choose data entry or view
    - Data entry:
      - A form field is presented for each `sosa:ObservableProperty` listed with the `qudt:QuantityKind` and `qudt:Unit` it should be given in
      - The submission time is recorded as the resultTime
    - Data view:
      - A table
        - Columns: the resultTime and one for each `sosa:ObservableProperty`
        - Rows: One for each `ssn:Stimulus`

## Database Key Design

Assuming all of this is present in `ex:`.

- `sosa:Sensor`/`foaf:Person`: `ex:users/<username>`
- `sosa:FeatureOfInterest`: `ex:features/<featurename>`
- `sosa:ObservableProperty`: `ex:properties/<featurename>/<propertyname>`
- `ssn:Stimulus`: `ex:stimuli/<featurename>/<resultTime>`
- `sosa:Observation`: `ex:observations/<featurename>/<propertyname>/<resultTime>`
- `sosa:Result`: `ex:results/<featurename>/<propertyname>/<resultTime>`

Everything else would be anonymous.
