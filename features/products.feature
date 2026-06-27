Feature: Product catalog administration

  Background:
    Given the following products
      | name        | description             | price | available | category   |
      | Apple       | Fresh red apple         | 1.99  | True      | FOOD       |
      | T-Shirt     | Cotton shirt            | 19.99 | True      | CLOTHS     |
      | Hammer      | Steel hammer            | 9.99  | False     | TOOLS      |
      | Pan         | Kitchen pan             | 14.99 | True      | HOUSEWARES |

  Scenario: Read a product
    When I visit the "Home Page"
    And I set the "Search ID" to "1"
    And I press the "Retrieve" button
    Then I should see "Apple" in the results

  Scenario: Update a product
    When I visit the "Home Page"
    And I set the "Search ID" to "1"
    And I press the "Retrieve" button
    And I set the "Name" to "Green Apple"
    And I press the "Update" button
    Then I should see "Green Apple" in the results

  Scenario: Delete a product
    When I visit the "Home Page"
    And I set the "Search ID" to "1"
    And I press the "Delete" button
    Then I should not see "Apple" in the results

  Scenario: List all products
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see "Apple" in the results
    And I should see "T-Shirt" in the results
    And I should see "Hammer" in the results
    And I should see "Pan" in the results

  Scenario: Search by name
    When I visit the "Home Page"
    And I set the "Name" to "Apple"
    And I press the "Search" button
    Then I should see "Apple" in the results
    And I should not see "Hammer" in the results

  Scenario: Search by category
    When I visit the "Home Page"
    And I select "FOOD" in the "Category" dropdown
    And I press the "Search" button
    Then I should see "Apple" in the results
    And I should not see "T-Shirt" in the results

  Scenario: Search by availability
    When I visit the "Home Page"
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see "Apple" in the results
    And I should see "T-Shirt" in the results
    And I should not see "Hammer" in the results
