import streamlit as st
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

# Line chart for values by year
line_chart = px.line(
    filtered_df,
    x='Year',
    y='Value',
    color='Type of Wages',
    color_discrete_sequence=['#DAA520'],
    title='Wages by Year'
)

line_chart.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ),
    yaxis_title='Wage',
)

st.plotly_chart(line_chart)

# Provide download button for filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='filtered_values_by_year.csv', mime='text/csv')
