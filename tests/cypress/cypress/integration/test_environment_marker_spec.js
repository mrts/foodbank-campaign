describe('Test environment should have descriptive "Test" mark', function () {
  it('Check the user page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/')
    cy.get('.page-header > h2:nth-child(2)').should('contain', 'TEST')
  })

  it('Check the admin login page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/haldus/')
    cy.get('#site-name > a:nth-child(1) > span:nth-child(1)').should('contain', 'TEST')
  })

  it('Check the admin main page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/haldus/')
    cy.get('#id_username').type(Cypress.env('admin_username'))
    cy.get('#id_password').type(Cypress.env('admin_password'))
    cy.get('.submit-row > input[type="submit"]').click()
    cy.get('#site-name > a:nth-child(1) > span:nth-child(1)').should('contain', 'TEST')
  })
})
