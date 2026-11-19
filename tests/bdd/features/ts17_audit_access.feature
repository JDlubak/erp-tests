@bdd
Feature: Audit trail access
  As a company I want only administrators to see the audit trail
  so that the change history stays confidential.

  Scenario Outline: BDD-07 Audit trail access depends on the admin role
    Given I am signed in as "<account>"
    When I open the dashboard
    Then I should see my dashboard
    And the Audit Trail link should be <link>
    When I go to the audit trail page
    Then I should see <result>

    Examples:
      | account    | link   | result                 |
      | admin      | shown  | the audit records      |
      | sales      | hidden | an access denied page  |
      | warehouse  | hidden | an access denied page  |
      | accountant | hidden | an access denied page  |
      | guest      | hidden | an access denied page  |
