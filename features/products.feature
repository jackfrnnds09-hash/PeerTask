# features/products.feature
Feature: Product Management
  As a user
  I want to manage products
  So that I can organize and track inventory

Background:
  Given I initialize the test environment


Scenario: Read a single product
  Given a product in the database with details:
    | name        | Laptop Pro           |
    | description | High-performance laptop |
    | price       | 1299.99              |
    | quantity    | 15                   |
    | category    | Electronics          |
  When I request to read the product with ID 1
  Then the response status should be 200
  And the product name should be "Laptop Pro"
  And the product price should be 1299.99
  And the product category should be "Electronics"


Scenario: Update a product
  Given a product in the database with details:
    | name      | Original Product    |
    | price     | 99.99              |
    | quantity  | 50                 |
    | category  | Electronics        |
  When I update the product with:
    | name      | Updated Product    |
    | price     | 149.99            |
    | quantity  | 30                |
  Then the response status should be 200
  And the product name should be "Updated Product"
  And the product price should be 149.99
  And the product quantity should be 30


Scenario: Delete a product
  Given a product in the database with details:
    | name      | Product to Delete  |
    | price     | 49.99             |
    | quantity  | 10                |
    | category  | Books             |
  When I delete the product with ID 1
  Then the response status should be 200
  And the product with ID 1 should not exist


Scenario: List all products
  Given I have the following products:
    | name          | description        | price | quantity | category    |
    | Laptop        | Portable computer  | 999.99| 10       | Electronics |
    | Phone         | Mobile device      | 699.99| 25       | Electronics |
    | Python Book   | Programming book   | 29.99 | 50       | Books       |
  When I request to list all products
  Then the response status should be 200
  And the products list should contain 3 items
  And the product list should include "Laptop"
  And the product list should include "Phone"
  And the product list should include "Python Book"


Scenario: Search products by name
  Given I have the following products:
    | name              | description        | price | quantity | category    |
    | Laptop Pro        | Premium laptop     | 1299.99| 5       | Electronics |
    | Laptop Basic      | Basic laptop       | 499.99 | 20      | Electronics |
    | Gaming Mouse      | Precision mouse    | 79.99  | 100     | Electronics |
  When I search for products with name "Laptop"
  Then the response status should be 200
  And the search results should contain 2 products
  And the results should include "Laptop Pro"
  And the results should include "Laptop Basic"
  And the results should not include "Gaming Mouse"


Scenario: Search products by name - exact match
  Given I have the following products:
    | name              | description        | price | quantity | category    |
    | Laptop Pro        | Premium laptop     | 1299.99| 5       | Electronics |
    | Laptop Pro Max    | Ultra premium      | 1699.99| 3       | Electronics |
  When I search for products with exact name "Laptop Pro"
  Then the response status should be 200
  And the search results should contain 1 product
  And the result should have name "Laptop Pro"


Scenario: Search products by category
  Given I have the following products:
    | name           | description        | price | quantity | category      |
    | Python Book    | Programming book   | 29.99 | 50       | Books         |
    | Java Book      | Java reference     | 39.99 | 30       | Books         |
    | Laptop         | Portable computer  | 999.99| 10       | Electronics   |
  When I search for products in category "Books"
  Then the response status should be 200
  And the search results should contain 2 products
  And the results should include "Python Book"
  And the results should include "Java Book"
  And all results should have category "Books"


Scenario: Search products by category - multiple categories
  Given I have the following products:
    | name              | description        | price | quantity | category    |
    | Laptop            | Portable computer  | 999.99| 10       | Electronics |
    | Phone             | Mobile device      | 699.99| 25       | Electronics |
    | Python Book       | Programming book   | 29.99 | 50       | Books       |
    | Monitor           | Display            | 349.99| 8        | Electronics |
  When I search for products in category "Electronics"
  Then the response status should be 200
  And the search results should contain 3 products
  And all results should have category "Electronics"
  And the results should include "Laptop"
  And the results should include "Phone"
  And the results should include "Monitor"


Scenario: Search available products (in stock)
  Given products with availability:
    | name           | quantity | available |
    | In Stock 1     | 100      | true      |
    | In Stock 2     | 50       | true      |
    | Out of Stock 1 | 0        | false     |
    | Low Stock      | 5        | true      |
  When I search for available products
  Then the response status should be 200
  And the search results should contain 3 products
  And the results should include "In Stock 1"
  And the results should include "In Stock 2"
  And the results should include "Low Stock"
  And the results should not include "Out of Stock 1"


Scenario: Search unavailable products (out of stock)
  Given products with availability:
    | name            | quantity | available |
    | In Stock        | 100      | true      |
    | Out of Stock 1  | 0        | false     |
    | Out of Stock 2  | 0        | false     |
  When I search for unavailable products
  Then the response status should be 200
  And the search results should contain 2 products
  And the results should include "Out of Stock 1"
  And the results should include "Out of Stock 2"
  And all results should have quantity 0


Scenario: Search products by availability with mixed results
  Given I have the following products:
    | name              | description        | price | quantity | category    |
    | Available Item 1  | In stock           | 50.00 | 100      | General     |
    | Available Item 2  | In stock           | 75.00 | 25       | General     |
    | Unavailable Item  | Out of stock       | 99.99 | 0        | General     |
  When I filter for products by availability "available"
  Then the response status should be 200
  And the search results should contain 2 products
  And all results should have quantity greater than 0
  When I filter for products by availability "unavailable"
  Then the response status should be 200
  And the search results should contain 1 product
  And all results should have quantity equal to 0
