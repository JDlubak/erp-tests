@bdd
Feature: Stock adjustment
  As a warehouse worker I want to correct the stock level so that the
  system matches the physical stock, but never below zero.

  Scenario: BDD-03 Surplus is posted and a loss above the stock is rejected
    Given I am authenticated in the API as "warehouse"
    And a new item with no stock
    When I post a stock surplus of 10 units
    Then the adjustment should be posted
    And the item should have 10 units on hand
    When I post a stock loss of 11 units
    Then the adjustment should be rejected as exceeding the stock
    And the item should have 10 units on hand
