import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from behave import given, when, then

def get_browser():
    browser_choice = os.getenv('BROWSER', 'chrome')  # Por defecto usa Chrome si no se especifica el navegador
    
    if browser_choice.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")  # Opcional: ejecuta sin interfaz gráfica
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=firefox_options)
    
    else:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")  # Opcional: ejecuta sin interfaz gráfica
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

@given('el usuario está en la página de inicio de sesión')
def step_impl(context):
    context.browser = get_browser()
    context.browser.get('http://localhost:5000/login')

@when('el usuario ingresa su nombre de usuario y contraseña correctos')
def step_impl(context):
    context.browser.find_element(By.NAME, 'username').send_keys('usuario')
    context.browser.find_element(By.NAME, 'password').send_keys('usuario1234')

@when('hace clic en el botón "Iniciar sesión"')
def step_impl(context):
    context.browser.find_element(By.XPATH, '//input[@type="submit"]').click()

@then('el usuario debe ser redirigido a la página principal')
def step_impl(context):
    assert 'Lista de Hospitales Registrados' in context.browser.page_source
    context.browser.quit()
