Feature: Login de usuario

  Scenario: Login exitoso
    Given el usuario está en la página de inicio de sesión
    When el usuario ingresa su nombre de usuario y contraseña correctos
    And hace clic en el botón "Iniciar sesión"
    Then el usuario debe ser redirigido a la página principal
