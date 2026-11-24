@bdd
Feature: Signing in with the login form
  As a user I want to sign in with my username and password so that I can
  use the application, and I want a clear error when the data is wrong.

  Scenario Outline: BDD-04 Signing in with correct credentials
    Given I am on the sign-in page
    When I sign in with username "<username>" and password "<username>"
    Then I should see my dashboard

    Examples:
      | username  |
      | admin     |
      | warehouse |
      | guest     |

  Scenario Outline: BDD-04 Signing in with incorrect credentials
    Given I am on the sign-in page
    When I sign in with username "<username>" and password "<password>"
    Then I should see the invalid credentials error
    And I should see the sign-in page

    Examples:
      | username     | password |
      | admin        | wrong    |
      | non_existent | admin    |
