@bdd
Feature: Purchase order lifecycle
  As a warehouse worker I want to take a purchase order through creation,
  confirmation and goods receipt so that the ordered goods end up in stock.

  Scenario: BDD-01 Purchase order from creation to goods receipt
    Given a new vendor and a new item
    And I am authenticated in the API as "warehouse"
    When I create a purchase order for 10 units at 5.00 each
    Then the purchase order should be saved as a draft for the vendor with 1 line
    When I confirm the purchase order
    Then the purchase order should be confirmed
    When I receive 10 units of the purchase order into stock
    Then the goods receipt should be posted
    And the purchase order should be received
