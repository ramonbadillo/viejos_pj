Feature: Administrar citas 

Scenario: Login into the system
  Given the URL "http://localhost:5000/appointments/"
  When I fill in field with id "username" with "hola@adios.com"
  And I fill in field with id "password" with "12345"
  And I submit the form

Scenario: Create an appoitment
  Given the URL "http://localhost:5000/appointments/create/"  
  When I fill in field with id "title" with "Junta con el viejo"
  And I fill in field with id "start" with "2014-10-15 15:00:00"
  And I fill in field with id "end" with "2014-10-15 16:00:00"
  And I fill in field with id "location" with "CIMAT"
  And I fill in field with id "description" with "El viejo se enoja si no llegan temprano"
  And I submit the form

Scenario: Consult an appoitment
  Given the URL "http://localhost:5000/appointments/2/"
  Then I see that the element with class "appointment-detail" contains "El viejo se enoja si no llegan temprano"

Scenario: Consult an appoitment that does not exist
  Given the URL "http://localhost:5000/appointments/0/"
  Then I see that the title of the page contains "Not Found"

Scenario: Edit a given appointment
  Given the URL "http://localhost:5000/appointments/2/edit"
  When I update the field with id "title" with "Viejos Appointment"
  And I submit the form
  Then I see that the element with class "appointment-detail" contains "Viejos Appointment"

Scenario: Edit a date given appointment
  Given the URL "http://localhost:5000/appointments/2/edit"
  When I update the field with id "start" with actual date
  And I submit the form
  Then I see that the element with class "appointment-detail" contains the actual date

Scenario: List all appoitments    
  Given the URL "http://localhost:5000/appointments/"
  Then I see at least "2" appoitments with the class "appointment-detail"

Scenario: Delete an appoitment  
  Given the URL "http://localhost:5000/appointments/"
  When I select the appointment with the title "Viejos Appointment"
  And I do click in the button "appointment-delete-link"    
  And the URL "http://localhost:5000/appointments/"  
  Then I see that the element with the class "appointment-detail" not contains "Cita con el dentista"