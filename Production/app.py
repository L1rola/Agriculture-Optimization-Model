import streamlit as st
import plotly.express as px
import numpy as np



# Set the app title

st.title('Sales Optimization')

# Add a welcome message

st.write('Welcome to the Jungle')

# Create a text input

user_input = st.number_input('Competition prices:', 1)

# Display the customized message

optimized_price = user_input * 1.5
optimized_price = round(optimized_price, 0)
optimized_price = int(optimized_price)
import plotly.express as px
import numpy as np

st.write(f'Optimized Price: {optimized_price}')



# Slider for selecting the number of data points

# data_points = st.slider('Number of data points', min_value=50, max_value=10000, value=500)

# Generate random data

data = np.random.randn(optimized_price * 10)

# Create a histogram using Plotly

fig = px.histogram(data, nbins=50, labels={'value': 'Data Points'}, title='Histogram of Random Data')

# Display the histogram

st.plotly_chart(fig)

