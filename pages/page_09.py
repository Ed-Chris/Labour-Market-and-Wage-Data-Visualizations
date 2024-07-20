import streamlit as st
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

# Line chart for gender pay gap over years
line_chart = px.line(
    filtered_df,
    x='Year',
    y='Gender Pay Gap (%)',
    color_discrete_sequence=['#DAA520'],
    title='Gender Pay Gap Over Years'
)

st.plotly_chart(line_chart)

# Provide download button for filtered data
csv = filtered_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='gender_pay_gap_over_years.csv', mime='text/csv')
