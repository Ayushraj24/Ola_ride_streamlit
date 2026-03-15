import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚖",
    layout="wide"
)

st.title("🚖 OLA Ride Insights Dashboard")


# -------------------------
# Load Data
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("/Users/ayushraj/Projects/Analysis/OLA ride/Data/ola_rides_cleaned.csv")
    return df


df = load_data()


# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

payment = st.sidebar.multiselect(
    "Payment Method",
    df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

df = df[
    (df["Vehicle_Type"].isin(vehicle)) &
    (df["Payment_Method"].isin(payment))
]


# -------------------------
# KPI Section
# -------------------------

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Rides",
    f"{len(df):,}"
)

col2.metric(
    "Total Revenue",
    f"₹{df[df['Booking_Status'] == 'success']['Booking_Value'].sum():,.0f}"
)

col3.metric(
    "Avg Ride Distance",
    round(df["Ride_Distance"].mean(), 2)
)

col4.metric(
    "Unique Customers",
    df["Customer_ID"].nunique()
)


# -------------------------
# Dataset Preview
# -------------------------

st.divider()
st.header("Dataset Preview")

st.dataframe(df.head(100))


# -------------------------
# Ride Trends
# -------------------------

st.divider()
st.header("Ride Trends")

col1, col2 = st.columns(2)

# Ride demand by hour
rides_hour = df.groupby("ride_hour").size().reset_index(name="rides")

fig1 = px.line(
    rides_hour,
    x="ride_hour",
    y="rides",
    markers=True,
    title="Ride Demand by Hour"
)

col1.plotly_chart(fig1, use_container_width=True)


# Ride demand by day
rides_day = df["ride_day"].value_counts().reset_index()
rides_day.columns = ["Day", "Rides"]

fig2 = px.bar(
    rides_day,
    x="Day",
    y="Rides",
    title="Ride Demand by Day"
)

col2.plotly_chart(fig2, use_container_width=True)


# -------------------------
# Revenue Analysis
# -------------------------

st.divider()
st.header("Revenue Analysis")

col1, col2 = st.columns(2)

revenue_vehicle = df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()

fig3 = px.bar(
    revenue_vehicle,
    x="Vehicle_Type",
    y="Booking_Value",
    title="Revenue by Vehicle Type"
)

col1.plotly_chart(fig3, use_container_width=True)


fig4 = px.histogram(
    df,
    x="Booking_Value",
    nbins=40,
    title="Ride Value Distribution"
)

col2.plotly_chart(fig4, use_container_width=True)


# -------------------------
# Cancellation Analysis
# -------------------------

st.divider()
st.header("Cancellation Analysis")

col1, col2 = st.columns(2)

status_counts = df["Booking_Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig5 = px.pie(
    status_counts,
    names="Status",
    values="Count",
    title="Ride Status Distribution"
)

col1.plotly_chart(fig5)


cancel_vehicle = df[df["Booking_Status"].str.contains("canceled", case=False)]

cancel_vehicle = cancel_vehicle.groupby("Vehicle_Type").size().reset_index(name="cancel_count")

fig6 = px.bar(
    cancel_vehicle,
    x="Vehicle_Type",
    y="cancel_count",
    title="Cancellations by Vehicle Type"
)

col2.plotly_chart(fig6, use_container_width=True)


# -------------------------
# Ratings Analysis
# -------------------------

st.divider()
st.header("Ratings Analysis")

col1, col2 = st.columns(2)

fig7 = px.histogram(
    df,
    x="Driver_Ratings",
    nbins=20,
    title="Driver Ratings Distribution"
)

col1.plotly_chart(fig7, use_container_width=True)


ratings_vehicle = df.groupby("Vehicle_Type")["Driver_Ratings"].mean().reset_index()

fig8 = px.bar(
    ratings_vehicle,
    x="Vehicle_Type",
    y="Driver_Ratings",
    title="Average Driver Rating by Vehicle Type"
)

col2.plotly_chart(fig8, use_container_width=True)