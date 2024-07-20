import streamlit as st
import plotly.express as px

# Content for Page 8
st.title("Wages - Average Values by Industry")

# Load cleaned data from session state
df_yearly_wages = st.session_state.df_yearly_wages

# Filter out 'Total employees, all wages' from Type of Wages options
type_of_wages_options = df_yearly_wages['Type of Wages'].unique()
type_of_wages_options = [opt for opt in type_of_wages_options if opt != 'Total employees, all wages']

# Selectbox widgets for filtering in the sidebar
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_yearly_wages['Characteristics'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly_wages['Age group'].unique())
selected_type_of_wages = st.sidebar.selectbox("Select Type of Wages", type_of_wages_options)

# Year range slider for filtering
year_range = st.sidebar.slider("Select Year Range", 
                               min_value=int(df_yearly_wages['Year'].min()), 
                               max_value=int(df_yearly_wages['Year'].max()), 
                               value=(int(df_yearly_wages['Year'].min()), int(df_yearly_wages['Year'].max())))

# Filter data based on selections and year range
filtered_df = df_yearly_wages[
    (df_yearly_wages['Characteristics'] == selected_characteristic) &
    (df_yearly_wages['Age group'] == selected_age_group) &
    (df_yearly_wages['Type of Wages'] == selected_type_of_wages) &
    (df_yearly_wages['Year'].astype(int) >= year_range[0]) &
    (df_yearly_wages['Year'].astype(int) <= year_range[1])
]

# Calculate average values by industry
avg_values_by_industry = filtered_df.groupby('Industry')['Value'].mean().reset_index()

# Sort data by 'Value' in descending order
avg_values_by_industry = avg_values_by_industry.sort_values(by='Value', ascending=False)

# Bar chart for average values by industry
bar_chart = px.bar(
    avg_values_by_industry,
    x='Industry',
    y='Value',
    color_discrete_sequence=['#DAA520'],
    title=f'Average Values by Industry from {year_range[0]} to {year_range[1]}'
)

bar_chart.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ),
    width=1000,  # Set the width of the chart
    height=600,  # Set the height of the chart
    yaxis_title='Wage',
)

st.plotly_chart(bar_chart, use_container_width=True)

# Provide download button for filtered data
csv = avg_values_by_industry.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name=f'average_values_by_industry_{year_range[0]}_{year_range[1]}.csv', mime='text/csv')
