from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the webpage
driver.get("https://www.fhalmeria.com/es/historico-mercados.aspx")

wait = WebDriverWait(driver, 10)

start_date = (datetime.today() - timedelta(days=0)).strftime("%d/%m/%Y")
end_date = (datetime.today() - timedelta(days=60)).strftime("%d/%m/%Y")

select_element = driver.find_element(By.ID, "contenedor_informacion_DDLLugares")
select_object = Select(select_element)
select_object.select_by_value("3")

date_input = driver.find_element_by_id('contenedor_informacion_TBFechaInicio')
date_input.clear()
date_input.send_keys(start_date) 

date_input = driver.find_element_by_id('contenedor_informacion_TBFechaFin')
date_input.clear()
date_input.send_keys(end_date) 

# Locate the submit button by its id
buscar_button = driver.find_element_by_id('contenedor_informacion_BBuscar')

# Click the submit button
buscar_button.click()

# Extract the prices for each day
submit_button = driver.find_element_by_id('contenedor_informacion_RBusqueda_BVerPizarra_0')

# Click the submit button
submit_button.click()

driver.quit()
