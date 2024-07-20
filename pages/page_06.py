import streamlit as st
import pandas as pd
import plotly.express as px

# Content for Page 6
st.title("Average Difference in Participation Rates by Industry")

# Load cleaned data from session state
processed_data = st.session_state.processed_data

# Selectbox widgets for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", processed_data['Characteristics'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", processed_data['Age group'].unique())

# Year range slider for filtering
year_range = st.sidebar.slider("Select Year Range", 
                               min_value=int(processed_data['Year'].min()), 
                               max_value=int(processed_data['Year'].max()), 
                               value=(int(processed_data['Year'].min()), int(processed_data['Year'].max())))

# Filter data based on selections and year range
filtered_df = processed_data[
    (processed_data['Characteristics'] == selected_characteristic) &
    (processed_data['Age group'] == selected_age_group) &
    (processed_data['Year'].astype(int) >= year_range[0]) &
    (processed_data['Year'].astype(int) <= year_range[1])
]

# Calculate the difference in participation rates if not already done
if 'Difference (%)' not in filtered_df.columns:
    filtered_df['Difference (%)'] = filtered_df['Male Participation Rate (%)'] - filtered_df['Female Participation Rate (%)']

# Calculate average difference by industry
average_diff_df = filtered_df.groupby('Industry', as_index=False)['Difference (%)'].mean()

# Sort data by 'Value' in descending order
average_diff_df = average_diff_df.sort_values(by='Difference (%)', ascending=False)

# Bar chart for average differences in participation rates by industry
bar_chart = px.bar(
    average_diff_df,
    x='Industry',
    y='Difference (%)',
    color_discrete_sequence=['#9E7F03'],
    title=f'Average Difference in Participation Rates by Industry from {year_range[0]} to {year_range[1]}',
    labels={'Difference (%)': 'Average Difference (%)'}
)

# Update layout for larger and wider chart
bar_chart.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ),
    width=800,  # Set the width of the chart
    height=600,  # Set the height of the chart
    xaxis=dict(tickangle=40),  # Tilt x-axis labels
    title={
        'text': f'Average Difference in Participation Rates by Industry from {year_range[0]} to {year_range[1]}'
    },
    xaxis_title='Industry',
    yaxis_title='Average Difference (%)',
    legend_title='Gender'
)

st.plotly_chart(bar_chart)

# Provide download button for filtered data
csv = average_diff_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name=f'average_difference_participation_rates_{year_range[0]}_{year_range[1]}.csv', mime='text/csv')
