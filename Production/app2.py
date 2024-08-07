import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import altair as alt
import os
from flask import Flask, request, jsonify



from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

print("Current Working Directory: ", os.getcwd())
print("Files in the directory: ", os.listdir())
os.chdir('production')

app = Flask(__name__)

# Carga tus datos
final = pd.read_csv('final.csv')
print(final)

# Configuración del modelo
rf = RandomForestRegressor(n_estimators=1000, min_samples_leaf=0.2)
X = final.drop('Price', axis=1)
y = final['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
rf.fit(X_train, y_train)

@app.route('/')
def home():
    return "API for Price Optimization Model"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    date_input = pd.to_datetime(data['date_input'])
    quantity_kilos = data['quantity_kilos']
    customer_name = data['customer_name']
    customer_price = data['customer_price']
    customer_kilos = data['customer_kilos']

           
    row = final[(final['Dia'] == date_input.day) & (final['Mes'] == date_input.month) & (final['Año'] == date_input.year)]

    if row.empty:
        return jsonify({"error": "No data available for this day"}), 400
        
        
    real_price = row['Price'].iloc[0] if 'Price' in row else None
    real_price = real_price / 100

    row = row.drop(columns=['Price'])

    prediction = rf.predict(row)
    prediction = prediction / 100
    predicted_value = prediction[0] if prediction.size > 0 else "Prediction not possible"

    
    customer_income = customer_price * customer_kilos
    profit = float((customer_price - real_price) * customer_kilos)

    result = {
        "predicted_price": round(predicted_value, 2),
        "real_price": round(real_price, 2),
        "quantity_kilos": int(quantity_kilos),
        "prediction_difference": round(real_price - predicted_value, 2),
        "customer_name": customer_name,
        "customer_price": round(customer_price, 2),
        "customer_kilos": int(customer_kilos),
        "customer_income": customer_income,
        "profit": round(profit, 2),
        "remaining_kilos": int(quantity_kilos - customer_kilos)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


predict_price_for_specific_date()
st.markdown(f'<span style="font-size:24px;">{"**Now we need to figure out how to recoup that loss.**"}</span>', unsafe_allow_html=True)
st.write("Now i'm gonna ask you for a daily benefit, to make it realistic, it should be between 0-5%")
benefit_target = st.number_input("Please enter the percentage of profit you would like to make:", min_value = 0.0, format='%f')

kgs_left = quantity_kilos - customer_kilos

def loss_recoup():
    if st.button('Target'):
        row = final[(final['Dia'] == date_input.day) & (final['Mes'] == date_input.month) & (final['Año'] == date_input.year)]
        row = row.drop('Price', axis = 1)
        prediction = rf.predict(row)
        prediction = prediction / 100
        predicted_value = prediction[0] if prediction.size > 0 else "Prediction not possible"          
        target = predicted_value + (predicted_value * (benefit_target / 100))
        st.write(f"Our sales target is: {round(target, 2)}€.")
        st.write(f"We have {round(kgs_left, 2)} left after supplying {customer_name}")
        st.write(f"Then we need a profit of {round(kgs_left * target, 2)}€ in order to recoup that loss.")

loss_recoup()

st.write("Normally, California pepper season goes from August to April.")
st.write(f'<span style="font-size:20px;">{"**Now, we are going to simulate a real situation where we will have different forecasts depending on the month of the year we are in.**"}</span>', unsafe_allow_html=True)
import itertools 
import random

months = ['September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']

def custom_distribution(size=8):
    if st.button('Show Dataframes'):
        values = np.zeros(size)
        middle_index = size // 2
        for i in range(size):
            if i < middle_index:
                values[i] = 750000 + (i / middle_index) * (6000000 - 750000)
            else:
                values[i] = 6000000 - ((i - middle_index) / middle_index) * (6000000 - 750000)

        forecast_dataframe = pd.DataFrame(values, index = months)
        st.write(forecast_dataframe)
        st.line_chart(forecast_dataframe)
        st.write('Once we have that, we are going to create a demand simulation from 4 big customers.')
        st.write("This demand will be correlated with each month's forecast.")
        bigc_monthly_demand = np.random.uniform(25000, 125000, 4)
        bigc_monthly_demand = bigc_monthly_demand.astype(int)
        total_bigc_demand = bigc_monthly_demand.sum()

        # Now, we scale each customer's demand to match the forecast distribution.
        # The assumption here is that the length of the forecast distribution is a multiple of the number of customers.
        scaled_demands = []
        for i in range(len(values) // len(bigc_monthly_demand)):
            # Calculate scaling factor for each segment of the forecast distribution
            scale_factors = values[i*len(bigc_monthly_demand):(i+1)*len(bigc_monthly_demand)] / total_bigc_demand
            # Scale each customer's demand and append to the scaled_demands list.
            scaled_demands.extend(bigc_monthly_demand * scale_factors)

        scaled_demands = np.array(scaled_demands).astype(int)
        initial_proportions = bigc_monthly_demand / total_bigc_demand


        scaled_monthly_demands = [initial_proportions * forecast for forecast in values]

        # Convertimos la lista a un array de numpy para una mejor manipulación y visualización
        scaled_monthly_demands = np.array(scaled_monthly_demands).astype(int)
        adjusted_forecast_distribution = values * 0.6

        # Calcular la nueva distribución de la demanda mensual ajustada entre los clientes, manteniendo las proporciones iniciales.
        adjusted_scaled_monthly_demands = [initial_proportions * adjusted_forecast for adjusted_forecast in adjusted_forecast_distribution]

        # Convertir a array de numpy y cambiar el tipo a entero.
        adjusted_scaled_monthly_demands = np.array(adjusted_scaled_monthly_demands).astype(int)
        client_names = ['BC1', 'BC2', 'BC3', 'BC4']


        month_indices = ['Septiembre', 'Octubre', 'Noviembre', 'Diciembre', 'Enero', 'Febrero', 'Marzo', 'Abril']

        # Crear el DataFrame
        demand_dataframe = pd.DataFrame(adjusted_scaled_monthly_demands, columns=client_names, index=month_indices)

        demand_dataframe['Total demand'] = demand_dataframe['BC1'] + demand_dataframe['BC2'] + demand_dataframe['BC3'] + demand_dataframe['BC4']
        demand_dataframe['Forecast'] = values
        demand_dataframe['Remaining Kilos'] = demand_dataframe['Forecast'] - demand_dataframe['Total demand']
        demand_dataframe = demand_dataframe.rename(columns={'BC1':'BC1 kgs', 'BC2':'BC2 kgs', 'BC3':'BC3 kgs', 'BC4':'BC4 kgs'})
        # st.write(demand_dataframe)
        row = final[(final['Dia'] == date_input.day) & (final['Mes'] == date_input.month) & (final['Año'] == date_input.year)]
        row = row.drop('Price', axis = 1)
        prediction = rf.predict(row)
        prediction = prediction / 100
        predicted_value = prediction[0] if prediction.size > 0 else "Prediction not possible"          
        target = predicted_value + (predicted_value * (benefit_target / 100))
    
        st.write(demand_dataframe)

        # Rango de precios
        price_range = (0.85, 1.25)

        # Crear precios ficticios para cada cliente
        prices = np.random.uniform(low=price_range[0], high=price_range[1], size=len(client_names))

        # Convertir los precios a un DataFrame para visualizarlos mejor
        price_dataframe = pd.DataFrame(prices, index=client_names, columns=['Price per kg'])
        prices_for_clients = {client: np.round(np.random.uniform(low=price_range[0], 
                                                            high=price_range[1], 
                                                            size=len(month_indices)), 2)
                        for client in client_names}

        # Convertir el diccionario de precios en un DataFrame
        prices_dataframe = pd.DataFrame(prices_for_clients, index=month_indices)
        prices_dataframe.index = demand_dataframe.index

        # Ahora concatenamos los precios al DataFrame de demanda
        complete_dataframe = pd.concat([demand_dataframe, prices_dataframe], axis=1)
        st.write('Now these 4 customers give us their offers that produce an income.')

        complete_dataframe['BC1_income'] = complete_dataframe['BC1 kgs'] * complete_dataframe['BC1']
        complete_dataframe['BC2_income'] = complete_dataframe['BC2 kgs'] * complete_dataframe['BC1']
        complete_dataframe['BC3_income'] = complete_dataframe['BC3 kgs'] * complete_dataframe['BC3']
        complete_dataframe['BC4_income'] = complete_dataframe['BC4 kgs'] * complete_dataframe['BC4']

        st.write(complete_dataframe)

        st.write(f'Before we established a benefit of {round(target, 2)}€, therefore we need to calculate how much that would be before supplying this customers (if the percentage of profit is changed, final target will change as well).')

        complete_dataframe['Total Target'] = target * complete_dataframe['Forecast']
        complete_dataframe['Total Target'] = complete_dataframe['Total Target'].astype(int)

        st.write("We have to calculate the total income obtain by the 4 big customers")
        complete_dataframe['BCTotal_income'] = complete_dataframe['BC1_income'] + complete_dataframe['BC2_income'] + complete_dataframe['BC3_income'] + complete_dataframe['BC4_income']
        complete_dataframe['Diff'] = complete_dataframe['Total Target'] - complete_dataframe['BCTotal_income']
        st.write(complete_dataframe[['BCTotal_income', 'Diff']])

        st.write("In the diff column we have the amount remaining to our target")

        st.write("Our model is going to generate distributions based in customer offers, remaining product and target.")
    


custom_distribution()



import numpy as np
import random

# Los precios ficticios generados
prices = np.random.uniform(1.20, 1.50, 8) # These are the prices we should obtain in order to reach the target. 

# Nombres de los clientes (a modo de ejemplo)
c_names = ['Customer1', 'Customer2', 'Customer3', 'Customer4', 'Customer5', 'Customer6', 'Customer7', 'Customer8']

# Diferencias de ingresos y kilos restantes por mes
TT_difference = {
    'October': 478662,
    'November': 1298514,
    'December': 2066937,
    'January': 2624325,
    'February': 4142155,
    'March': 3122836,
    'April': 2355746,
    'May': 1310650
}

remaining_kgs_values = np.array([300002, 825002, 1350003, 1875003, 2400003, 1875003, 1350003, 825002])

# Meses para referencia
months = ['October', 'November', 'December', 'January', 'February', 'March', 'April', 'May']

def distribucion_aleatoria(prices, remaining_kgs, income_target, intentos=20000000, num_distribuciones=3, max_diferencia=10000000):
    
    mejores_distribuciones = []
    
    for _ in range(intentos):
        distribucion = np.random.uniform(0, 1, len(prices)) * remaining_kgs
        if distribucion.sum() > remaining_kgs:
            continue
        total_ingresos = np.dot(prices, distribucion)
        diferencia = abs(income_target - total_ingresos)

        if diferencia < max_diferencia:
            mejores_distribuciones.append((distribucion, diferencia))
    
    # Ordenar las distribuciones por la diferencia más pequeña
    mejores_distribuciones.sort(key=lambda x: x[1])

    # Mantener solo las mejores num_distribuciones distribuciones
    mejores_distribuciones = mejores_distribuciones[:num_distribuciones]

    return [d[0] for d in mejores_distribuciones], [d[1] for d in mejores_distribuciones]

# El resto del código permanece igual.

results = [] 


def distribuciones_por_mes(month):
    month_index = months.index(month)
    remaining_kgs = remaining_kgs_values[month_index]
    income_target = TT_difference[month]
        
        # Buscar distribuciones que se acerquen al objetivo de ingresos
    mejores_distribuciones, mejores_diferencias = distribucion_aleatoria(
        prices, remaining_kgs, income_target)

    # Imprimir las distribuciones encontradas junto con los nombres
    for i, distribucion in enumerate(mejores_distribuciones, 1):
        distribucion_texto = f"Distribución {i}:"
        for nombre, price, kilos in zip(c_names, prices, distribucion):
           distribucion_texto += f"\n{nombre}: {round(kilos, 2)}kgs a {round(price, 2)}€"
        distribucion_texto += f"\nTarget difference: {round(mejores_diferencias[i-1], 2)}€\n"
        results.append(distribucion_texto)
    return results if results else "No valid distributions found"

# Ejemplo de uso para el mes de 'Enero'
st.write(f'<span style="font-size:16px;">{"**Months going from October to May.**"}</span>', unsafe_allow_html=True)
user_input3 = st.text_input("Please enter the month which you want to obtain the distributions: ")
if user_input3:
    distribuciones = distribuciones_por_mes(user_input3)
    st.write(distribuciones)