import streamlit as st
import plotly.express as px

st.title("Labour Market - Industry Data")

# Load cleaned data from session state
df_yearly = st.session_state.df_yearly

# Sidebar filters using selectbox
selected_characteristic = st.sidebar.selectbox("Select Characteristics", df_yearly['Characteristics'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly['Age group'].unique())

# Year range slider for filtering
year_range = st.sidebar.slider("Select Year Range", 
                               min_value=int(df_yearly['Year'].min()), 
                               max_value=int(df_yearly['Year'].max()), 
                               value=(int(df_yearly['Year'].min()), int(df_yearly['Year'].max())))

# Filter the DataFrame based on selected options and year range
filtered_df = df_yearly[
    (df_yearly['Characteristics'] == selected_characteristic) &
    (df_yearly['Age group'] == selected_age_group) &
    (df_yearly['Year'].astype(int) >= year_range[0]) &
    (df_yearly['Year'].astype(int) <= year_range[1])
]

# Group by Industry and Sex, then calculate the mean of the Value column
grouped_df = filtered_df.groupby(['Industry', 'Sex'], as_index=False)['Value'].mean()

# Sort data by 'Value' in descending order
grouped_df = grouped_df.sort_values(by='Value', ascending=False)

# Plotly bar chart
fig = px.bar(grouped_df, x='Industry', y='Value', color='Sex', barmode='group', title=f'Average Characteristics Values by Industry from {year_range[0]} to {year_range[1]}')

# Adjust chart size and legend position
fig.update_layout(
    yaxis_title='Characteristics (x1000)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.0,
        xanchor="left",
        x=0.6
    ),
    width=1200,  # Set the width of the chart
    height=600,  # Set the height of the chart
    xaxis=dict(tickangle=45)  # Tilt x-axis labels
)

st.plotly_chart(fig, use_container_width=True)  # Adjust width to fit container

# Download button for filtered data CSV
csv = grouped_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name=f'filtered_data_{year_range[0]}_{year_range[1]}.csv', mime='text/csv')
