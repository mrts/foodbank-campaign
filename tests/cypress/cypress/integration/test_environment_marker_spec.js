describe('Test environment should have descriptive "Test" mark', function () {
  it('Check the user page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/')
    cy.get('.page-header > h2:nth-child(2)').should('contain', 'TEST')
  })

  it('Check the admin page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/haldus/')
    cy.get('#site-name > a:nth-child(1) > span:nth-child(1)').should('contain', 'TEST')
  })
})
