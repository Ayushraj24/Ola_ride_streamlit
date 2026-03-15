import streamlit as st
import pandas as pd

st.title("SQL Query Analysis")

# Load data
df = pd.read_csv("/Users/ayushraj/Projects/Analysis/OLA ride/Data/ola_rides_cleaned.csv")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
"Successful Bookings",
"Avg Distance per Vehicle",
"Customer Cancellations",
"Top Customers",
"Driver Cancellations",
"Prime Sedan Ratings",
"UPI Payments",
"Avg Customer Rating",
"Total Booking Value",
"Incomplete Rides"
])

# 1 Successful Bookings
with tab1:

    st.subheader("Retrieve all successful bookings")

    st.code("""
SELECT *
FROM ola_rides
WHERE Booking_Status = 'success';
""", language="sql")

    result = df[df["Booking_Status"] == "success"]

    st.write("Total Successful Rides:", result.shape[0])

    st.dataframe(result.head(100))


# 2 Average Distance
with tab2:

    st.subheader("Average ride distance per vehicle type")

    st.code("""
SELECT Vehicle_Type,
AVG(Ride_Distance)
FROM ola_rides
GROUP BY Vehicle_Type;
""", language="sql")

    result = df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index()

    st.dataframe(result)


# 3 Customer Cancellations
with tab3:

    st.subheader("Total cancelled rides by customers")

    st.code("""
SELECT COUNT(*)
FROM ola_rides
WHERE Booking_Status = 'canceled by customer';
""", language="sql")

    result = df[df["Booking_Status"] == "canceled by customer"].shape[0]

    st.metric("Cancelled by Customers", result)


# 4 Top Customers
with tab4:

    st.subheader("Top 5 customers with highest rides")

    st.code("""
SELECT Customer_ID,
COUNT(*) as total_rides
FROM ola_rides
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;
""", language="sql")

    result = (
        df.groupby("Customer_ID")
        .size()
        .reset_index(name="Total_Rides")
        .sort_values("Total_Rides", ascending=False)
        .head(5)
    )

    st.dataframe(result)


# 5 Driver Cancellations
with tab5:

    st.subheader("Driver cancellations")

    st.code("""
SELECT COUNT(*)
FROM ola_rides
WHERE Booking_Status = 'canceled by driver';
""", language="sql")

    result = df[df["Booking_Status"] == "canceled by driver"].shape[0]

    st.metric("Driver Cancelled Rides", result)


# 6 Prime Sedan Ratings
with tab6:

    st.subheader("Maximum and Minimum driver ratings for Prime Sedan")

    st.code("""
SELECT MAX(Driver_Ratings), MIN(Driver_Ratings)
FROM ola_rides
WHERE Vehicle_Type = 'Prime Sedan';
""", language="sql")

    sedan = df[df["Vehicle_Type"] == "prime sedan"]

    col1, col2 = st.columns(2)

    col1.metric("Max Rating", round(sedan["Driver_Ratings"].max(),2))
    col2.metric("Min Rating", round(sedan["Driver_Ratings"].min(),2))


# 7 UPI Payments
with tab7:

    st.subheader("Rides where payment method is UPI")

    st.code("""
SELECT *
FROM ola_rides
WHERE Payment_Method = 'upi';
""", language="sql")

    result = df[df["Payment_Method"] == "upi"]

    st.write("Total UPI Rides:", result.shape[0])

    st.dataframe(result.head(100))


# 8 Avg Customer Rating
with tab8:

    st.subheader("Average customer rating per vehicle type")

    st.code("""
SELECT Vehicle_Type,
AVG(Customer_Rating)
FROM ola_rides
GROUP BY Vehicle_Type;
""", language="sql")

    result = df.groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index()

    st.dataframe(result)


# 9 Total Booking Value
with tab9:

    st.subheader("Total booking value of successful rides")

    st.code("""
SELECT SUM(Booking_Value)
FROM ola_rides
WHERE Booking_Status = 'success';
""", language="sql")

    result = df[df["Booking_Status"] == "success"]["Booking_Value"].sum()

    st.metric("Total Booking Value", f"₹{result:,.0f}")


# 10 Incomplete Rides
with tab10:

    st.subheader("Incomplete rides with reason")

    st.code("""
SELECT Booking_ID, Incomplete_Rides_Reason
FROM ola_rides
WHERE Incomplete_Rides = 1;
""", language="sql")

    result = df[df["Incomplete_Rides"] == 1][
        ["Booking_ID", "Incomplete_Rides_Reason"]
    ]

    st.dataframe(result)