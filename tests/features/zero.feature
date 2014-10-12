Feature: Appointments

Scenario: Login into the system
  Given I go to "http://127.0.0.1:5000/appointments/"
  When I fill in field with id "username" with "hola@adios.com"
  And I fill in field with id "password" with "12345"
  And I submit the form