import streamlit as st
import plotly.express as px

st.title("Yearly Labour Market Data")

# Load cleaned data from session state
df_yearly = st.session_state.df_yearly

# Sidebar filters using selectbox
selected_characteristic = st.sidebar.selectbox("Select Characteristic", df_yearly['Characteristics'].unique())
selected_industry = st.sidebar.selectbox("Select Industry", df_yearly['Industry'].unique())
selected_sex = st.sidebar.selectbox("Select Sex", df_yearly['Sex'].unique())
selected_age_group = st.sidebar.selectbox("Select Age Group", df_yearly['Age group'].unique())

# Filter the DataFrame based on selected options
filtered_df = df_yearly[
        (df_yearly['Characteristics'] == selected_characteristic) &
        (df_yearly['Industry'] == selected_industry) &
        (df_yearly['Sex'] == selected_sex) &
        (df_yearly['Age group'] == selected_age_group)
]

fig = px.line(filtered_df, x='Year', y='Value', color='Characteristics', title='Yearly Characteristics Values',color_discrete_sequence=['#DAA520'])

# Update the layout to move the legend to the top of the chart
fig.update_layout(
    yaxis_title='Number of people (x1000)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    )
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

csv = filtered_df.to_csv(index=False)
st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')
