import streamlit as st
import pandas as pd
import plotly.express as px

# Content for Page 5
st.title("Labour Market - Average Participation Rates by Industry")

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

# Calculate average participation rates by industry
average_participation_rates = filtered_df.groupby('Industry', as_index=False).agg({
    'Male Participation Rate (%)': 'mean',
    'Female Participation Rate (%)': 'mean'
})

# Sort data by 'Value' in descending order
average_participation_rates = average_participation_rates.sort_values(by=['Male Participation Rate (%)', 'Female Participation Rate (%)'], ascending=[False, False])

# Reshape the data for plotting
average_participation_rates = average_participation_rates.melt(id_vars='Industry', 
                                                              value_vars=['Male Participation Rate (%)', 'Female Participation Rate (%)'], 
                                                              var_name='Gender', 
                                                              value_name='Average Participation Rate (%)')

# Bar chart for average participation rates by industry
bar_chart = px.bar(
    average_participation_rates,
    x='Industry',
    y='Average Participation Rate (%)',
    color='Gender',
    barmode='group',
    title=f'Average Participation Rates by Industry from {year_range[0]} to {year_range[1]}',
    labels={'Average Participation Rate (%)': 'Average Participation Rate (%)'}
)

# Update layout for larger and wider chart
bar_chart.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=0.5
    ),
    width=1500,  # Set the width of the chart
    height=600,  # Set the height of the chart
    xaxis=dict(tickangle=45),  # Tilt x-axis labels
    title={
        'text': f'Average Participation Rates by Industry from {year_range[0]} to {year_range[1]}'
    },
    xaxis_title='Industry',
    yaxis_title='Average Participation Rate (%)',
    legend_title='Gender'
)

st.plotly_chart(bar_chart)

# Provide download button for filtered data
csv = average_participation_rates.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name=f'average_participation_rates_by_industry_{year_range[0]}_{year_range[1]}.csv', mime='text/csv')
