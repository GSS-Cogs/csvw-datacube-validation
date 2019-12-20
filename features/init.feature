
Feature: The validation framework works as expected

  Scenario: The app initialises with the expected defaults
  Given I initialise the app with an argument of schema "/resources/simple.csv--schema.json"
  Then the config contains the keys: "options,stages"
  And the function map contains the function "csvlint"

  Scenario: The app accepts local reference information via a yaml file
  Given I initialise the app with an argument of schema "/resources/simple-schema.json"
  And specify a local reference file of "/resources/simple-local-ref.yaml"
  Then I have local references for: "my-file,that-file,this-folder"

  Scenario: Given a schema, the app can create a job
  Given I initialise the app with an argument of schema "/resources/simple-schema.json"
  And I create a validation task from that schema
  Then the derrived observation file path ends with "simple-observation-file.csv"
  And the observation csv for job "0" can be loaded into pandas