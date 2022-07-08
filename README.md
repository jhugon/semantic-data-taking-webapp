# Semantic Data Taking Web-app

This app is a Flask-based dynamic website that uses an RDF graph database to store data. Initially, the website is for manually entering data into HTML forms. The entered data can then be viewed in tables.

## Example Scenario

A simple example of usage would be to collect data on the fuel economy of a car. When filling up a car, the user would enter the odometer reading and amount of fuel put into the car.

## Ontology Design

Custom classes are prefixed with `sdtw`.

- Mainly based on the [Semantic Sensor Network Ontology](https://www.w3.org/TR/vocab-ssn/)
  - In this case the data-entering user, `sdtw:User`, would be of type `sosa:Sensor` and also either a `foaf:Person` or `vcard:Individual`
  - The particular car would be of type `sosa:FeatureOfInterest`
  - The odometer reading would be a `sdtw:Property`, a subclass of `sosa:ObservableProperty`
    - Each record of the odometer reading would be a `sosa:Observation` with the the value `sosa:hasResult` and recording time `sosa:resultTime` (a `xsd:dateTime`)
      - I'd like to include units, so the `sosa:Result` could also be of type `qudt:Quantity` from [QUDT](https://www.qudt.org/) and be given a `qudt:unit` and the actual value would be stored as a `qudt:value`
    - The `sdtw:Property` should also `sdtw:hasQuantityKind` and possibly `sdtw:hasUnit` the `sosa:Observable` should be given in
  - The amount of fuel put in the car would be another `sosa:ObservableProperty`
    - Observations would be made similar to with the odometer reading
  - What links together one particular odometer reading and amount of fuel is the same `ssn:Stimulus`.
    - The stimulus would `sdtw:hasTime` the same timestamp as the observations have as resultTime
    
## User Interface Design

*Assuming the schema for a data taking scenario is already in the database for now*

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

- `sdtw:User`: `ex:users/<username>`
- `sosa:FeatureOfInterest`: `ex:features/<featurename>`
- `sdtw:Property`: `ex:properties/<featurename>/<propertyname>`
- `ssn:Stimulus`: `ex:stimuli/<featurename>/<resultTime>`
- `sosa:Observation`: `ex:observations/<featurename>/<propertyname>/<resultTime>`
- `sosa:Result`: `ex:results/<featurename>/<propertyname>/<resultTime>`

Everything else would be anonymous.
