Feature: Registro de Hospitales


    Scenario: Agregar un nuevo hospital exitosamente
        Given el usuario esta en la pagina de registro de hospital
        When el usuario ingresa los datos del hospital
        And hace click en el boton "Registrar"
        Then el hospital debe aparecer en la lista de hospitales registrados