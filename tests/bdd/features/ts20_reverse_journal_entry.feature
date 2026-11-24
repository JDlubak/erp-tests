@bdd
Feature: Reversing a manual journal entry
  As an accountant I want to reverse a manual posting, but only once,
  so that mistakes can be corrected without duplicating the correction.

  Scenario: BDD-02 A manual entry can be reversed only once
    Given I am authenticated in the API as "accountant"
    And a manual journal entry of 100.00
    When I reverse the journal entry
    Then a posted reversal with the same totals should be created
    When I reverse the journal entry
    Then the reversal should be rejected as already reversed
