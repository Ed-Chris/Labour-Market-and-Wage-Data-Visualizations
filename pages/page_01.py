import streamlit as st
import plotly.graph_objects as go
from prophet import Prophet
import pandas as pd

st.title("Yearly Labour Market Data")

# Load cleaned data from session state
df_yearly = st.session_state.df_yearly

# Sidebar filters using selectbox
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_yearly['Characteristics'].unique())
selected_industry = st.sidebar.selectbox("Select Industry", df_yearly['Industry'].unique())
selected_sex = st.sidebar.selectbox("Select Sex", df_yearly['Sex'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly['Age group'].unique())

# Filter the DataFrame based on selected options
filtered_df = df_yearly[
    (df_yearly['Characteristics'] == selected_characteristic) &
    (df_yearly['Industry'] == selected_industry) &
    (df_yearly['Sex'] == selected_sex) &
    (df_yearly['Age group'] == selected_age_group)
]

# Ensure Year column is of datetime type and set to January of each year
filtered_df['Year'] = pd.to_datetime(filtered_df['Year'].astype(str) + '-01-01 00:00:00')

# Prepare data for Prophet
forecast_df = filtered_df[['Year', 'Value']].rename(columns={'Year': 'ds', 'Value': 'y'})

# Initialize and fit Prophet model
model = Prophet()
model.fit(forecast_df)

# Make future dataframe for 10 years, starting from January each year
future = model.make_future_dataframe(periods=10, freq='Y')
forecast = model.predict(future)

# Ensure forecast 'ds' column is of datetime type and set to January of each year
forecast['ds'] = pd.to_datetime(forecast['ds'].dt.year.astype(str) + '-01-01 00:00:00')

# Filter out the forecast values that fall within the historical data range
last_historical_year = filtered_df['Year'].max()
forecast_combined = forecast[['ds', 'yhat']].rename(columns={'ds': 'Year', 'yhat': 'Forecasted Value'})
forecast_combined = forecast_combined[forecast_combined['Year'] > last_historical_year]

# Combine historical and forecasted data for visualization
historical_df = filtered_df[['Year', 'Value']].rename(columns={'Value': 'Historical Value'})
combined_df = pd.concat([historical_df, forecast_combined[['Year', 'Forecasted Value']]], ignore_index=True)

# Plot combined data in a single chart with different colors
fig = go.Figure()

# Add historical data trace
fig.add_trace(go.Scatter(
    x=historical_df['Year'],
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
    line=dict(color='blue')
))

# Update layout
fig.update_layout(
    title='Yearly Labour Market Data and Forecast',
    xaxis_title='Year',
    yaxis_title='Number of people (x1000)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Combine historical and forecast data for download
combined_csv = combined_df.to_csv(index=False)
st.download_button(label="Download CSV", data=combined_csv, file_name='combined_data.csv', mime='text/csv')
