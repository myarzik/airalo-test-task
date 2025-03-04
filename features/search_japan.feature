Feature: Search for an eSIM package in Japan
  As a user
  I want to search for a Japan eSIM package
  So that I can check its details before purchasing

  Scenario: User searches for a Japan eSIM package
    Given the user opens the Airalo homepage
    When the user searches for "Japan"
    And selects the first paid eSIM package
    Then the package PACKAGE_TITLE should be "Moshi Moshi"
    Then the package COVERAGE should be "Japan"
    Then the package DATA should be "1 GB"
    Then the package VALIDITY should be "7 Days"
    Then the package PRICE should be "$4.50 USD"