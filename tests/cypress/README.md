# Cypress.io tests for foodbank-campaign

Setup:

    npm install

Run Cypress:

    node_modules/.bin/cypress open

Press *Run All Tests* or click the test you wish to run

## Passing sensitive data to tests

Pass sensitive data with environment variables with *cypress.env.json* file:
    
    {
        "admin_username": "user",
        "admin_password": "password"
    }
