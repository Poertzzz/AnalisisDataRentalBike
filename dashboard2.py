import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

hour_df = pd.read_csv("CleanData.csv")

mnth_list = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
hour_df["mnth"] = pd.Categorical(hour_df["mnth"], categories=mnth_list, ordered=True)

st.title("Bike Rental Dashboard")

st.sidebar.header("Filters")
season_filter = st.sidebar.selectbox("Select Season", ['All'] + list(hour_df['season'].unique()))

filtered_data = hour_df if season_filter == 'All' else hour_df[hour_df['season'] == season_filter]


st.subheader("Bike Rentals per Season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=filtered_data, ax=ax)
st.pyplot(fig)

st.subheader("Casual vs Registered Users per Season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='registered', data=filtered_data, color='blue', label='Registered')
sns.barplot(x='season', y='casual', data=filtered_data, color='orange', label='Casual')
plt.legend()
st.pyplot(fig)

st.subheader("Feature Correlation Heatmap")
numeric_columns = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
correlation_matrix = hour_df[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

st.subheader("Bike Rentals per Hour")
data_hourly = hour_df.groupby('hr')[['cnt']].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=data_hourly, marker='o', ax=ax)
st.pyplot(fig)


st.subheader("Bike Rentals per Month")
data_bulanan = hour_df.groupby('mnth')[['cnt', 'registered', 'casual']].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='mnth', y='cnt', data=data_bulanan, marker='o', color='g', label='Total')
sns.lineplot(x='mnth', y='registered', data=data_bulanan, marker='o', color='b', label='Registered')
sns.lineplot(x='mnth', y='casual', data=data_bulanan, marker='o', color='orange', label='Casual')
plt.xlabel("Month")
st.pyplot(fig)

st.subheader("Weather Impact on Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
sns.pointplot(data=hour_df, x='hr', y='cnt', hue='weathersit', ax=ax)
st.pyplot(fig)

st.sidebar.write("Dashboard created with Streamlit")
