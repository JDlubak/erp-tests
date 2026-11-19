@bdd
Feature: Sales order lifecycle
  As a company I want to take a sales order through confirmation, shipment
  and invoicing so that the customer receives the goods and is billed.

  Scenario: BDD-05 Sales order from creation to invoice
    Given a new customer and a sales item with 10 units in stock
    And I am authenticated in the API as "sales"
    When I create a sales order for 2 units at 50.00 each
    Then the sales order should be saved as a draft for the customer with 1 line
    When I confirm the sales order
    Then the sales order should be confirmed
    Given I am authenticated in the API as "warehouse"
    When I ship 2 units of the sales order from stock
    Then the shipment should be registered
    Given I am authenticated in the API as "accountant"
    When I invoice 2 units of the sales order at 50.00 each
    Then the invoice should be issued for the sales order
