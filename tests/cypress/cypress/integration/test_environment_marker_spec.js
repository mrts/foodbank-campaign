describe('Test environment should have descriptive "Test" mark', function () {
  it('Check the user page "Test" mark', function () {
    cy.visit('https://test-osale.toidupank.ee/')
    cy.get('.page-header > h2:nth-child(2)').should('contain', 'TEST')
  })
  
  //it('Check the admin page "Test" mark', function () {
  //  cy.visit('https://test-osale.toidupank.ee/')
  //  cy.title().should('include', 'Kitchen Sink')
  //})
})