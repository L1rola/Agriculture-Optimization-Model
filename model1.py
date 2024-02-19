from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the webpage
driver.get("https://www.fhalmeria.com/es/historico-mercados.aspx")

wait = WebDriverWait(driver, 50)


start_date = (datetime.today() - timedelta(days=60)).strftime("%d/%m/%Y")
end_date = (datetime.today() - timedelta(days=0)).strftime("%d/%m/%Y")

# Search for an ID which is contenedor_informacion_DDLLugares. We're searching a specific element.
select_element = driver.find_element(By.ID, "contenedor_informacion_DDLLugares")
# This variable stores the previous element for later use.
select_object = Select(select_element)
# Uses select_object to select the option that has a value '3'. 3 = La Union.
select_object.select_by_value("3") 

# Finds an input filed with the ID 'contenedor_informacion_TBFechaInicio'
date_input = driver.find_element(By.ID, 'contenedor_informacion_TBFechaInicio')
# Before entering a new date, we need to clear the previous input.
date_input.clear()
# New date input.
date_input.send_keys(start_date) 

# Finds an input filed with the ID 'contenedor_informacion_TBFechaInicio'
date_input = driver.find_element(By.ID,'contenedor_informacion_TBFechaFin')
# Before entering a new date, we need to clear the previous input.
date_input.clear()
# New date input.
date_input.send_keys(end_date) 

# Locate the submit button by its id
# buscar_button = driver.find_element(By.ID,'contenedor_informacion_BBuscar')
# Reemplaza la línea directa de click con un WebDriverWait para esperar que el botón sea clickeable
buscar_button = wait.until(EC.element_to_be_clickable((By.ID,'contenedor_informacion_BBuscar')))

# Click the submit button
buscar_button.click()

# Extract the prices for each day
#submit_button = driver.find_element(By.ID, 'contenedor_informacion_RBusqueda_BverPizarra_0')

# Esperar a que los elementos que contienen los precios sean visibles
precios_elements = WebDriverWait(driver, 20).until(
    EC.visibility_of_all_elements_located((By.XPATH, "//td[starts-with(@data-title, 'Precio')]"))
)

# Extraer los precios de cada elemento encontrado
precios = [elem.text for elem in precios_elements]

print(precios)  # Imprimir los precios obtenidos

# ... Resto de tu código ...


# Click the submit button
#submit_button.click()

time.sleep(10)

driver.quit()
