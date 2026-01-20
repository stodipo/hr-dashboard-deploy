import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. DATA GENERATION (Mock Data)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Simulate a dataset of 500 employees
    np.random.seed(42)
    data = {
        'Employee_ID': range(1001, 1501),
        'Department': np.random.choice(['Sales', 'Engineering', 'HR', 'Marketing', 'Finance'], 500),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 500),
        'Gender': np.random.choice(['Male', 'Female'], 500),
        'Age': np.random.randint(22, 60, 500),
        'Tenure_Years': np.random.randint(1, 15, 500),
        'Performance_Score': np.random.choice([1, 2, 3, 4, 5], 500, p=[0.05, 0.1, 0.5, 0.25, 0.1]),
        'Attrition': np.random.choice(['Yes', 'No'], 500, p=[0.15, 0.85])
    }
    return pd.DataFrame(data)

df = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Data")
department_filter = st.sidebar.multiselect(
    "Select Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Apply filters
df_selection = df.query(
    "Department == @department_filter & Region == @region_filter"
)

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD (KPIs)
# -----------------------------------------------------------------------------
st.title("👥 Workforce Overview Dashboard")
st.markdown("##")

# Calculate Metrics
total_employees = len(df_selection)
avg_tenure = round(df_selection["Tenure_Years"].mean(), 1)
avg_age = round(df_selection["Age"].mean(), 1)

# Attrition Rate Calculation
attrition_count = len(df_selection[df_selection["Attrition"] == "Yes"])
attrition_rate = (attrition_count / total_employees * 100) if total_employees > 0 else 0

# Display KPIs in Columns
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", f"{total_employees}", "People")
col2.metric("Attrition Rate", f"{attrition_rate:.1f}%", "-2% vs Last Year")
col3.metric("Avg Tenure", f"{avg_tenure} Years", "Stable")
col4.metric("Avg Age", f"{avg_age} Years", "Avg")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. CHARTS & VISUALIZATIONS
# -----------------------------------------------------------------------------
col_left, col_right = st.columns(2)

# Chart 1: Employee Distribution by Department
with col_left:
    st.subheader("Headcount by Department")
    fig_dept = px.bar(
        df_selection['Department'].value_counts().reset_index(),
        x='Department',
        y='count',
        text='count',
        template="plotly_white",
        color='Department'
    )
    st.plotly_chart(fig_dept, use_container_width=True)

# Chart 2: Attrition vs Retention (Pie Chart)
with col_right:
    st.subheader("Attrition Distribution")
    fig_attrition = px.pie(
        df_selection,
        names='Attrition',
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.RdBu,
    )
    st.plotly_chart(fig_attrition, use_container_width=True)

# Chart 3: Performance by Tenure (Scatter)
st.subheader("Performance Score vs Tenure")
fig_scatter = px.scatter(
    df_selection,
    x="Tenure_Years",
    y="Performance_Score",
    color="Department",
    size="Age",
    hover_data=['Employee_ID'],
    template="plotly_white"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. DATA TABLE
# -----------------------------------------------------------------------------
with st.expander("View Underlying Data"):
    st.dataframe(df_selection)