# Import Libraries 

import pandas as pd 
import streamlit as st 
import plotly.express as px 

# Load Dataset 

data = pd.read_csv("covid_19_india.csv") 
st.write("Dataset Preview", data.head()) 

# Data Preprocessing 

# Convert Date column 
data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d') 

# Rename columns for easy use 
data = data.rename(columns={ 
    "State/UT": "State", 
    "Cured": "Recovered" 
}) 
 
# Drop missing values 
data = data.dropna() 

# Create Interactive UI 

st.title(" COVID-19 India Dashboard") 
 
# State filter 
states = data['State'].unique() 
selected_state = st.selectbox("Select State/UT", states) 
 
# Date filter 
start_date = st.date_input("Start Date", data['Date'].min()) 
end_date = st.date_input("End Date", data['Date'].max())


# Filter Data 

filtered_data = data[ 
    (data['State'] == selected_state) & 
    (data['Date'] >= pd.to_datetime(start_date)) & 
    (data['Date'] <= pd.to_datetime(end_date)) 
] 


# Line Chart (Trend Analysis) 

fig = px.line( 
    filtered_data, 
    x='Date', 
    y=['Confirmed', 'Active', 'Recovered', 'Deaths'], 
    title=f"COVID-19 Trends in {selected_state}" 
) 
 
st.plotly_chart(fig) 

#Bar Chart (Latest Status) 

latest_data = filtered_data.iloc[-1] 
 
fig_bar = px.bar( 
    x=['Confirmed', 'Active', 'Recovered', 'Deaths'], 
    y=[ 
        latest_data['Confirmed'], 
        latest_data['Active'], 
        latest_data['Recovered'], 
        latest_data['Deaths'] 
    ], 
    title="Latest COVID-19 Status" 
) 
 
st.plotly_chart(fig_bar) 

# Display Key Metrics 

st.subheader(" Key Metrics") 
 
st.metric("Confirmed", int(latest_data['Confirmed'])) 
st.metric("Active", int(latest_data['Active'])) 
st.metric("Recovered", int(latest_data['Recovered'])) 
st.metric("Deaths", int(latest_data['Deaths'])) 
 
st.metric("Recovery Rate (%)", round(latest_data['Recovery rate'], 2)) 
st.metric("Mortality Rate (%)", round(latest_data['Mortality rate'], 2)) 