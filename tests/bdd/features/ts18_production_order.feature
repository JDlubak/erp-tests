@bdd
Feature: Production order lifecycle
  As a warehouse worker I want to run a production order through its
  states so that finished goods are produced.

  Scenario: BDD-06 Production order from release to completion
    Given I am authenticated in the API as "warehouse"
    And a draft production order for 5 units
    When I release the production order
    Then the production order should be released
    When I issue the materials for the production order from stock
    Then the materials should be issued
    When I complete the production order with 5 units produced
    Then the production order should be done
