@bdd
Feature: Cancelling a production order
  As a warehouse worker I want to cancel a released production order
  so that production that is no longer needed is stopped.

  Scenario: BDD-06 Released production order can be cancelled
    Given I am authenticated in the API as "warehouse"
    And a released production order for 5 units
    When I cancel the production order
    Then the production order should be cancelled
