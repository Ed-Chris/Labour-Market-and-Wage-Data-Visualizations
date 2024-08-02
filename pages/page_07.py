import streamlit as st
import plotly.graph_objects as go
from prophet import Prophet
import pandas as pd
import plotly.express as px

# Content for Page 7
st.title("Yearly Wages Data")

# Load cleaned data from session state
df_yearly_wages = st.session_state.df_yearly_wages

# Filter out 'Total employees, all wages' from Type of Wages options
type_of_wages_options = df_yearly_wages['Type of Wages'].unique()
type_of_wages_options = [opt for opt in type_of_wages_options if opt != 'Total employees, all wages']

# Selectbox widgets for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_yearly_wages['Characteristics'].unique())
selected_industry = st.sidebar.selectbox("Select Industry", df_yearly_wages['Industry'].unique())
selected_sex = st.sidebar.selectbox("Select Sex", df_yearly_wages['Sex'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly_wages['Age group'].unique())
selected_type_of_wages = st.sidebar.selectbox("Select Type of Wages", type_of_wages_options)

# Filter data based on selections
filtered_df = df_yearly_wages[
    (df_yearly_wages['Characteristics'] == selected_characteristic) &
    (df_yearly_wages['Industry'] == selected_industry) &
    (df_yearly_wages['Sex'] == selected_sex) &
    (df_yearly_wages['Age group'] == selected_age_group) &
    (df_yearly_wages['Type of Wages'] == selected_type_of_wages)
]

# Ensure Year column is of datetime type and set to January of each year
filtered_df['Year'] = pd.to_datetime(filtered_df['Year'].astype(str) + '-01-01')

# Prepare data for Prophet
forecast_df = filtered_df[['Year', 'Value']].rename(columns={'Year': 'ds', 'Value': 'y'})

# Initialize and fit Prophet model
model = Prophet()
model.fit(forecast_df)

# Make future dataframe for 10 years
future = model.make_future_dataframe(periods=10, freq='Y')
forecast = model.predict(future)

# Ensure forecast 'ds' column is of datetime type and set to January of each year
forecast['ds'] = pd.to_datetime(forecast['ds'].dt.year.astype(str) + '-01-01')

# Filter out the forecast values that fall within the historical data range
last_historical_year = forecast_df['ds'].max()
forecast_combined = forecast[['ds', 'yhat']].rename(columns={'ds': 'Year', 'yhat': 'Forecasted Value'})
forecast_combined = forecast_combined[forecast_combined['Year'] > last_historical_year]

# Combine historical and forecasted data for visualization
historical_df = forecast_df[['ds', 'y']].rename(columns={'y': 'Historical Value'})
combined_df = pd.concat([historical_df, forecast_combined[['Year', 'Forecasted Value']]], ignore_index=True)

# Line chart for historical and forecasted values
fig = go.Figure()

# Add historical data trace
fig.add_trace(go.Scatter(
    x=historical_df['ds'],
    y=historical_df['Historical Value'],
    mode='lines',
    name='Historical Data',
    line=dict(color='orange')
))

# Add forecast data trace
fig.add_trace(go.Scatter(
    x=forecast_combined['Year'],
    y=forecast_combined['Forecasted Value'],
    mode='lines',
    name='Forecasted Data',
    line=dict(color='light blue')
))

# Update layout
fig.update_layout(
    title='Wages by Year and Forecast',
    xaxis_title='Year',
    yaxis_title='Wage in CAD',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig)

# Provide download button for filtered and forecasted data
combined_csv = combined_df.to_csv(index=False)
st.download_button(label="Download CSV", data=combined_csv, file_name='combined_wages_data.csv', mime='text/csv')
