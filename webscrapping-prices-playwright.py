from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


# Función para generar rangos de fechas por trimestres desde una fecha de inicio hasta hoy
def generate_date_ranges(start_date, end_date):
    current_date = start_date
    while current_date < end_date:
        yield current_date, min(current_date + timedelta(days=90), end_date)
        current_date += timedelta(days=91)

def run(playwright: Playwright, start_date: datetime, end_date: datetime) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    page = context.new_page()

    # Lista para almacenar los precios con su fecha correspondiente
    datos_pimiento = []

    # Iterar sobre los rangos de fechas generados
    for start, end in generate_date_ranges(start_date, end_date):
        # Formatea las fechas como strings
        start_str = start.strftime("%d-%m-%Y")
        end_str = end.strftime("%d-%m-%Y")

        # Navegar a la página con la tabla de precios
        page.goto("https://analytics.infoagro.com/pimiento-california-rojo")
        page.locator("#precio_select").select_option("9")
        page.get_by_placeholder("Rango de tiempo").click()
        page.get_by_placeholder("Rango de tiempo").fill(f"{start_str} a {end_str}")
        page.get_by_text("Buscar", exact=True).click()

        # Esperar a que la tabla de precios esté cargada
        page.wait_for_selector("#precios_tabla")

        # Obtener todas las filas de la tabla de precios
        rows = page.query_selector_all("#precios_tabla > tbody > tr")

        for row in rows:
            # Extraer la fecha de la primera celda (th) y el precio de la segunda celda (td)
            fecha = row.query_selector("th").text_content().strip()
            precio_texto = row.query_selector("td").text_content().strip()

            # Limpiar el texto del precio y convertirlo a un número entero (en céntimos)
            precio = int(float(precio_texto.split(' ')[0].replace(',', '.')) * 100)

            # Guardar la fecha y el precio en la lista de datos
            datos_pimiento.append((fecha, precio))

    # Imprimir los datos recopilados
    for fecha, precio in datos_pimiento: # Compilamos ambos elementos en una misma lista.
        print(fecha, precio)

    df = pd.DataFrame(datos_pimiento, columns = ['Date' , 'Price']) # Pasamos los datos a un dataframe para poder usarlos próximamente.
    print(df)

    df.to_csv('/Users/marcos/agrodata.csv', index = False)

    context.close()
    browser.close()

# Fecha de inicio para la recopilación de datos
start_date = datetime(2020, 1, 1)
# Fecha de hoy para finalizar la recopilación de datos
end_date = datetime.now()

with sync_playwright() as playwright:
    run(playwright, start_date, end_date)