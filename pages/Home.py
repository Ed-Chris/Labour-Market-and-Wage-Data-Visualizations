import streamlit as st

st.title("Home")

# Custom horizontal navigation bar using st.radio
selected_section = st.radio(
    "Navigation",
    ["About", "Insights", "Dependencies", "Tools used", "References"],
    horizontal=True
)

# Update session state based on the selected section
st.session_state.section = selected_section

# Content based on the selected section
if st.session_state.section == "About":
    # Define the about section using Markdown
    about_text = """
    ## About This Project

    This Streamlit application explores and visualizes labor force characteristics, wages, and gender pay gap data sourced from Statistics Canada (StatsCan). The app features 10 interactive visualizations spread across different pages:

    1. **Interactive Line Charts and Bar Graphs:** Explore trends in employment and wages over time, by industry, sex, and age group.
    2. **Gender Participation Rates:** Analyze participation rates by gender across different industries and age groups.
    3. **Gender Pay Gap Analysis:** Visualize and understand the gender pay gap trends across industries and over time.

    Each visualization allows you to dynamically select and compare data based on various criteria, providing insights into Canada's labor market dynamics.
    """

    # Streamlit app pages and other components should be defined below

    # Display the about section in your Streamlit app
    st.markdown(about_text)
elif st.session_state.section == "Insights":
    st.write("Here are some insights...")
elif st.session_state.section == "Dependencies":
    # Define the about section using Markdown
    about_depend = """
    ## Dependencies Used in the Project

    1. **pandas== 2.2.2**
    2. **plotly== 5.22.0**
    3. **stats_can== 2.6.3**
    4. **streamlit== 1.36.0**

    """

    # Display the about section in your Streamlit app
    st.markdown(about_depend)
elif st.session_state.section == "Tools used":
    st.write("We used the following tools...")
elif st.session_state.section == "References":
    st.write("Here are the references...")
