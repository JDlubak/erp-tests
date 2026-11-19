@bdd
Feature: Signing out
  As a user I want signing out to end my session
  so that nobody can use the application on my behalf afterwards.

  Scenario: BDD-08 Signing out ends the session and protects pages
    Given I am signed in as "sales"
    When I open the dashboard
    Then I should see my dashboard
    When I sign out
    Then I should see the sign-in page
    When I try to open the sales page
    Then I should be redirected to the sign-in page
    When I try to open the home page
    Then I should see the sign-in page
