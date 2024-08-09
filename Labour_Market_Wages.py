import streamlit as st
import pandas as pd
from stats_can import StatsCan
import plotly.graph_objs as go
   
def clean_data():
    sc = StatsCan()

    # Load and clean labour data
    df = sc.table_to_df("14-10-0023-01")
    df_clean = df[['REF_DATE', 'Labour force characteristics', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
    df_main = df_clean.rename(columns={
        'REF_DATE': 'Year',
        'Labour force characteristics': 'Characteristics',
        'North American Industry Classification System (NAICS)': 'Industry',
        'VALUE': 'Value'
    })
    df_main['Year'] = df_main['Year'].astype(str).str[:4]
    df_main['Industry'] = df_main['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()
    df_yearly = df_main.groupby(['Year', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False, observed=False).mean()

    # Filter and process employment data
    selected_characteristics = ['Employment', 'Full-time employment', 'Part-time employment']
    employment_data = df_yearly[df_yearly['Characteristics'].isin(selected_characteristics)]
    pivot_table = employment_data.pivot_table(index=['Year', 'Industry', 'Age group', 'Characteristics'], columns='Sex', values='Value')
    pivot_table['Male Participation Rate (%)'] = (pivot_table['Males'] / pivot_table['Both sexes']) * 100
    pivot_table['Female Participation Rate (%)'] = (pivot_table['Females'] / pivot_table['Both sexes']) * 100
    pivot_table.reset_index(inplace=True)
    processed_data = pivot_table[['Year', 'Industry', 'Age group', 'Characteristics', 'Male Participation Rate (%)', 'Female Participation Rate (%)']]
    processed_data['Difference (%)'] = processed_data['Male Participation Rate (%)'] - processed_data['Female Participation Rate (%)']

    # Load and clean wage data
    df_wages = sc.table_to_df("14-10-0064-01")
    df_clean_wages = df_wages[['REF_DATE', 'Wages', 'Type of work', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
    df_main_wages = df_clean_wages.rename(columns={
        'REF_DATE': 'Year',
        'Wages': 'Type of Wages',
        'Type of work': 'Characteristics',
        'North American Industry Classification System (NAICS)': 'Industry',
        'VALUE': 'Value'
    })
    df_main_wages['Year'] = df_main_wages['Year'].astype(str).str[:4]
    df_main_wages['Industry'] = df_main_wages['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()
    df_yearly_wages = df_main_wages.groupby(['Year', 'Type of Wages', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False, observed=False).mean()

    # Function to calculate the gender pay gap
    def calculate_gender_pay_gap(df):
        # Pivot the table to have separate columns for Male and Female wages
        df_pivot = df.pivot_table(index=['Year', 'Industry', 'Type of Wages', 'Characteristics', 'Age group'], columns='Sex', values='Value', aggfunc='mean').reset_index()
    
        # Calculate Gender Pay Ratio and Gender Pay Gap
        df_pivot['Gender Pay Ratio'] = df_pivot['Females'] / df_pivot['Males']
        df_pivot['Gender Pay Gap (%)'] = (1 - df_pivot['Gender Pay Ratio']) * 100
    
        return df_pivot

    # Get unique types of wages
    unique_types_of_wages = df_yearly_wages['Type of Wages'].unique()

    # Initialize an empty DataFrame to store combined results
    df_combined_gender_pay_gap = pd.DataFrame()

    # Process and combine results for each type of wage
    for wage_type in unique_types_of_wages:
        df_filtered = df_yearly_wages[df_yearly_wages['Type of Wages'] == wage_type]
        df_gender_pay_gap = calculate_gender_pay_gap(df_filtered)
    
        # Add the type of wage as a column for clarity
        df_gender_pay_gap['Type of Wages'] = wage_type
    
        # Concatenate the results to the combined DataFrame
        df_combined_gender_pay_gap = pd.concat([df_combined_gender_pay_gap, df_gender_pay_gap], ignore_index=True)

    # Store cleaned data in session state
    st.session_state.df_yearly = df_yearly
    st.session_state.processed_data = processed_data
    st.session_state.df_yearly_wages = df_yearly_wages
    st.session_state.df_combined_gender_pay_gap = df_combined_gender_pay_gap

clean_data()


# Main page content
st.title("Labour Market and Wage Characteristics Data Visualizations")
st.write("Select the pages for Visualizations. The filters for adjusting the parameters of the visualizations will appear on the sidebar.")

st.title("Hierarchy of Industries")
st.write("The below SunBurst chart shows how the industries are classified in different sectors")

# Data for the chart
labels = [
    "Industries", 
    "Goods-producing sector", "Services-producing sector", "Unclassified industries",
    "Agriculture", "Forestry, fishing, mining, quarrying, oil and gas", "Utilities", "Construction", "Manufacturing",
    "Wholesale and retail trade", "Transportation and warehousing", "Finance, insurance, real estate, rental and leasing", "Professional, scientific and technical services", 
    "Business, building and other support services", "Educational services", "Health care and social assistance", "Information, culture and recreation", "Accommodation and food services",
    "Other services (except public administration)", "Public administration",
    "Forestry and logging and support activities for forestry", "Fishing, hunting and trapping", "Mining, quarrying, and oil and gas extraction",
    "Durables", "Non-durables", 
    "Wholesale trade", "Retail trade",
    "Finance and insurance", "Real estate and rental and leasing"
]

parents = [
    "", 
    "Industries", "Industries", "Industries",
    "Goods-producing sector", "Goods-producing sector", "Goods-producing sector", "Goods-producing sector", "Goods-producing sector",
    "Services-producing sector", "Services-producing sector", "Services-producing sector", "Services-producing sector", 
    "Services-producing sector", "Services-producing sector", "Services-producing sector", "Services-producing sector", "Services-producing sector",
    "Services-producing sector", "Services-producing sector",
    "Forestry, fishing, mining, quarrying, oil and gas", "Forestry, fishing, mining, quarrying, oil and gas", "Forestry, fishing, mining, quarrying, oil and gas",
    "Manufacturing", "Manufacturing",
    "Wholesale and retail trade", "Wholesale and retail trade",
    "Finance, insurance, real estate, rental and leasing", "Finance, insurance, real estate, rental and leasing"
]

# Define distinct colors for each label
colors = [
    '#0083F9', '#ff7f0e', '#2ca02c', '#d62728', '#FFD180', '#FFAB91', '#F8BBD0', '#FF8A65', '#FF9800',
    '#98FF98', '#98FB98', '#90EE90', '#F0FFF0', '#00FA9A', '#32CD32', '#228B22', '#2E8B57', '#6B8E23',
    '#556B2F', '#013220', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#f7b6d2', '#7f7f7f',
    '#c5b0d5', '#ff9896', '#c49c94', '#f7b6d2', '#c7c7c7', '#d62728', '#9467bd'
]

# Create the Sunburst diagram
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    branchvalues="total",
    marker=dict(colors=colors)
))

# Update layout for better readability and larger size
fig.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    height=800,  # Adjust the height as needed
    width=800    # Adjust the width as needed
)

st.plotly_chart(fig)
