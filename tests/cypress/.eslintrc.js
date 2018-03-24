// https://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true, 
  plugins: [
    'cypress'
  ],
  env: {
    'cypress/globals': true
  },
  // https://github.com/standard/standard/blob/master/docs/RULES-en.md
  extends: 'standard'
}