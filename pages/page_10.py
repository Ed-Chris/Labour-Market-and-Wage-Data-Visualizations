import streamlit as st
import pandas as pd
import plotly.express as px

# Content for Page 10
st.title("Gender Pay Gap by Industry")

# Load cleaned data from session state
df_combined_gender_pay_gap = st.session_state.df_combined_gender_pay_gap

# Filter out 'Total employees, all wages' from Type of Wages options
type_of_wages_options = df_combined_gender_pay_gap['Type of Wages'].unique()
type_of_wages_options = [opt for opt in type_of_wages_options if opt != 'Total employees, all wages']

# Selectbox widget for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_combined_gender_pay_gap['Characteristics'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_combined_gender_pay_gap['Age group'].unique())
selected_type_of_wages = st.sidebar.selectbox("Select Type of Wages", type_of_wages_options)

# Year range slider for filtering
year_range = st.sidebar.slider("Select Year Range", 
                               min_value=int(df_combined_gender_pay_gap['Year'].min()), 
                               max_value=int(df_combined_gender_pay_gap['Year'].max()), 
                               value=(int(df_combined_gender_pay_gap['Year'].min()), int(df_combined_gender_pay_gap['Year'].max())))

# Filter data based on selections
filtered_df = df_combined_gender_pay_gap[
    (df_combined_gender_pay_gap['Characteristics'] == selected_characteristic) &
    (df_combined_gender_pay_gap['Age group'] == selected_age_group) &
    (df_combined_gender_pay_gap['Type of Wages'] == selected_type_of_wages) &
    (df_combined_gender_pay_gap['Year'].astype(int) >= year_range[0]) &
    (df_combined_gender_pay_gap['Year'].astype(int) <= year_range[1])
]

# Calculate average gender pay gap by industry
avg_gender_pay_gap_by_industry = filtered_df.groupby('Industry')['Gender Pay Gap (%)'].mean().reset_index()

# Sort data by 'Value' in descending order
avg_gender_pay_gap_by_industry = avg_gender_pay_gap_by_industry.sort_values(by='Gender Pay Gap (%)', ascending=False)

# Bar chart for average gender pay gap by industry
bar_chart = px.bar(
    avg_gender_pay_gap_by_industry,
    x='Industry',
    y='Gender Pay Gap (%)',
    title=f'Average Gender Pay Gap by Industry from {year_range[0]} to {year_range[1]}',
    color_discrete_sequence=['#DAA520']
)

bar_chart.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="left",
        x=0.6
    ),
    width=1000,  # Set the width of the chart
    height=600,  # Set the height of the chart
    xaxis=dict(tickangle=40)  # Tilt x-axis labels
)

# Adjust chart size
st.plotly_chart(bar_chart, use_container_width=True)  # Adjust width to fit container

# Provide download button for filtered data
csv = avg_gender_pay_gap_by_industry.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name=f'average_gender_pay_gap_by_industry_{year_range[0]}_{year_range[1]}.csv', mime='text/csv')
