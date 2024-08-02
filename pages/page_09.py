import streamlit as st
import plotly.graph_objects as go
from prophet import Prophet
import pandas as pd
import plotly.express as px

# Content for Page 9
st.title("Gender Pay Gap Over Years")

# Load cleaned data from session state
df_combined_gender_pay_gap = st.session_state.df_combined_gender_pay_gap

# Filter out 'Total employees, all wages' from Type of Wages options
type_of_wages_options = df_combined_gender_pay_gap['Type of Wages'].unique()
type_of_wages_options = [opt for opt in type_of_wages_options if opt != 'Total employees, all wages']

# Selectbox widgets for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_combined_gender_pay_gap['Characteristics'].unique())
selected_type_of_wages = st.sidebar.selectbox("Select Type of Wages", type_of_wages_options)
selected_age_group = st.sidebar.selectbox("Select Age Group", df_combined_gender_pay_gap['Age group'].unique())
selected_industry = st.sidebar.selectbox("Select Industry", df_combined_gender_pay_gap['Industry'].unique())

# Filter data based on selections
filtered_df = df_combined_gender_pay_gap[
    (df_combined_gender_pay_gap['Characteristics'] == selected_characteristic) &
    (df_combined_gender_pay_gap['Type of Wages'] == selected_type_of_wages) &
    (df_combined_gender_pay_gap['Age group'] == selected_age_group) &
    (df_combined_gender_pay_gap['Industry'] == selected_industry)
]

# Ensure Year column is of datetime type and set to January of each year
filtered_df['Year'] = pd.to_datetime(filtered_df['Year'].astype(str) + '-01-01')

# Prepare data for Prophet
forecast_df = filtered_df[['Year', 'Gender Pay Gap (%)']].rename(columns={'Year': 'ds', 'Gender Pay Gap (%)': 'y'})

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
forecast_combined = forecast[['ds', 'yhat']].rename(columns={'ds': 'Year', 'yhat': 'Forecasted Gender Pay Gap (%)'})
forecast_combined = forecast_combined[forecast_combined['Year'] > last_historical_year]

# Combine historical and forecasted data for visualization
historical_df = forecast_df[['ds', 'y']].rename(columns={'y': 'Historical Gender Pay Gap (%)'})
combined_df = pd.concat([historical_df, forecast_combined[['Year', 'Forecasted Gender Pay Gap (%)']]], ignore_index=True)

# Line chart for historical and forecasted gender pay gap
fig = go.Figure()

# Add historical data trace
fig.add_trace(go.Scatter(
    x=historical_df['ds'],
    y=historical_df['Historical Gender Pay Gap (%)'],
    mode='lines',
    name='Historical Data',
    line=dict(color='orange')
))

# Add forecast data trace
fig.add_trace(go.Scatter(
    x=forecast_combined['Year'],
    y=forecast_combined['Forecasted Gender Pay Gap (%)'],
    mode='lines',
    name='Forecasted Data',
    line=dict(color='light blue')
))

# Update layout
fig.update_layout(
    title='Gender Pay Gap Over Years and Forecast',
    xaxis_title='Year',
    yaxis_title='Gender Pay Gap (%)',
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
st.download_button(label="Download Combined Data CSV", data=combined_csv, file_name='combined_gender_pay_gap_data.csv', mime='text/csv')
