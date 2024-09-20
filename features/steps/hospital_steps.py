from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

#inicializar el navegador antes de cada escenario
def before_scenario(context, scenario):
    service = ChromeService(ChromeDriverManager().install())
    context.browser = webdriver.Chrome(service = service)
    
#cerrar el navegador despues de cada scenario
def after_scnario(context, scenario):
    context.browser.quit()

@given('el usuario esta en la pagina de registro de hospital')
def step_impl(context):
    context.browser.get('http://localhost:5000/register')
    
@when('el usuario ingresa los datos del hospital')
def step_impl(context):
    #simula la interaccion de un usuario llenando los campos
    context.browser.find_element(By.NAME, 'nombre').send_keys('Hospital General')
    context.browser.find_element(By.NAME, 'direccion').send_keys('123 calle Principal')
    context.browser.find_element(By.Name, 'telefono').send_keys('555-1234')

@when('hace click en el boton "Registrar"')
def step_impl(context):
    #Hace click en el botn registrar
    context.browser.find_element(By.XPATH, '//input[@type="submit"]').click()

@then('el hospital debe aparecer en la lista de hospitales registrados')
def step_impl(context):
    # Esperar a que la página redirija a la lista de hospitales
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'li'))  # Verifica que aparezca una lista
    )
    # Verificar que el hospital registrado esté en la página
    page_content = context.browser.page_source
    assert 'Hospital General' in page_content
    assert '123 Calle Principal' in page_content
    assert '555-1234' in page_content