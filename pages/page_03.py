import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Labour Market - Industry Data through the years")

# Load cleaned data from session state
df_yearly = st.session_state.df_yearly

# Sidebar filters using selectbox and slider
selected_characteristic = st.sidebar.selectbox("Select Characteristics", df_yearly['Characteristics'].unique())
selected_sex = st.sidebar.selectbox("Select Sex", df_yearly['Sex'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly['Age group'].unique())

# Year range slider for filtering
year_range = st.sidebar.slider("Select Year Range", 
                               min_value=int(df_yearly['Year'].min()), 
                               max_value=int(df_yearly['Year'].max()), 
                               value=(int(df_yearly['Year'].min()), int(df_yearly['Year'].max())))

# Convert 'Year' column to integers
df_yearly['Year'] = df_yearly['Year'].astype(int)

# Filter the DataFrame based on selected options and year range
filtered_df = df_yearly[
    (df_yearly['Characteristics'] == selected_characteristic) &
    (df_yearly['Sex'] == selected_sex) &
    (df_yearly['Age group'] == selected_age_group) &
    (df_yearly['Year'] >= year_range[0]) &
    (df_yearly['Year'] <= year_range[1])
]

# Sort data by 'Value' in descending order
filtered_df = filtered_df.sort_values(by='Value', ascending=False)

# Plotly bar chart
fig = px.bar(filtered_df, x='Year', y='Value', color='Industry', barmode='group', 
             title=f'Characteristics Values by Year and Industry ({year_range[0]} to {year_range[1]})')

# Set plotly chart size
fig.update_layout(yaxis_title='Characteristics (x1000)',showlegend=False,height=400, width=800)  # Adjust height and width as needed

# Display the chart in the main area
st.plotly_chart(fig)

# Download button for filtered data CSV
csv = filtered_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
