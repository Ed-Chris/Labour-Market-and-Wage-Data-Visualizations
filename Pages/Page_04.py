import streamlit as st
import plotly.express as px

# Content for Page 4
st.title("Labour Market Participation Rate")

# Load cleaned data from session state
processed_data = st.session_state.processed_data

# Selectbox widgets for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", processed_data['Characteristics'].unique())
selected_industry = st.sidebar.selectbox("Select Industry", processed_data['Industry'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", processed_data['Age group'].unique())

# Filter data based on selections
filtered_df = processed_data[
    (processed_data['Characteristics'] == selected_characteristic) &
    (processed_data['Industry'] == selected_industry) &
    (processed_data['Age group'] == selected_age_group)
]

# Line chart for participation rates
line_chart = px.line(filtered_df, x='Year', y=['Male Participation Rate (%)', 'Female Participation Rate (%)'], 
                     color_discrete_map={'Male Participation Rate (%)': '#0060F9', 'Female Participation Rate (%)': '#FD0ADF'},
                     title='Participation Rates Over Years')

# Update the layout to move the legend to the top of the chart
line_chart.update_layout(
    yaxis_title='Participation Rate (%)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="left",
        x=0.5
    )
)

st.plotly_chart(line_chart, use_container_width=True)

# Provide download button for filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='filtered_participation_rates.csv', mime='text/csv')
