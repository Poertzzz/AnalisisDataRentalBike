import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
jam = pd.read_csv('MainData.csv')
jam['dteday'] = pd.to_datetime(jam['dteday'])

# Sidebar for Filtering
st.sidebar.header("Filter Data")

start_date = pd.to_datetime("2011-01-01")
end_date = pd.to_datetime("2012-12-31")
jam = jam[(jam['dteday'] >= start_date) & (jam['dteday'] <= end_date)]

date_range = st.sidebar.date_input("Select Date Range", [start_date, end_date])
if date_range:
    start = pd.to_datetime(date_range[0])
    end = pd.to_datetime(date_range[1])
    jam = jam[(jam['dteday'] >= start) & (jam['dteday'] <= end)]

weather_mapping = {
    1: "Cerah",
    2: "Berkabut",
    3: "Hujan Ringan",
    4: "Hujan Lebat"
}
jam['weathersit'] = jam['weathersit'].map(weather_mapping)

weather_order = ["Cerah", "Berkabut", "Hujan Ringan", "Hujan Lebat"]

jam['weathersit'] = pd.Categorical(
    jam['weathersit'],
    categories=weather_order,
    ordered=True
)

weather_filter = st.sidebar.multiselect("Filter by Weather", jam['weathersit'].unique())
if weather_filter:
    jam = jam[jam['weathersit'].isin(weather_filter)]

### Tampilkan Pivot Table

pivot_table = jam.pivot_table(
    index='dteday',
    values=['casual', 'registered', 'cnt'],  # Atur urutan yang diinginkan
    aggfunc='sum'
)

pivot_table = pivot_table.reindex(['casual', 'registered', 'cnt'], level=0, axis=1)

st.subheader("Pivot Table Penyewaan Sepeda")
st.write(pivot_table)

### Pertanyaan 1: Mencari pendapatan tertinggi dari dua tipe user lalu menentukan strategi marketing untuk memaksimalkan pendapatan

st.title("Analisis Penyewaan Sepeda")

st.subheader("Total Penyewa per Tipe User")
total_user = pd.DataFrame({
    'Tipe User': ['Casual', 'Registered'],
    'Total Penyewa': [jam['casual'].sum(), jam['registered'].sum()]
})

fig, ax = plt.subplots()
sns.barplot(x='Tipe User', y='Total Penyewa', data=total_user, palette={'Casual':'orange', 'Registered':'blue'}, ax=ax)
st.pyplot(fig)

### Pertanyaan 2: Melihat Jumlah penyewaan berdasarkan waktu

st.subheader("Tren Penyewaan berdasarkan Jam")
fig, ax = plt.subplots()
sns.lineplot(x=jam['hr'], y=jam['cnt'], color='green', label='TOTAL', marker='o', linestyle='-')
sns.lineplot(x=jam['hr'], y=jam['registered'], color='blue', label='REGISTERED', marker='o', linestyle='-')
sns.lineplot(x=jam['hr'], y=jam['casual'], color='orange', label='CASUAL', marker='o', linestyle='-')
ax.set_xlabel('Jam')
ax.set_ylabel('Total Penyewa')
ax.set_title('Tren Penyewaan berdasarkan jam')
ax.legend()
plt.xticks(range(0, 24))
st.pyplot(fig)



### Pertanyaan 3: Melihat pengaruh cuaca terhadap jumlah pengguna

st.subheader("Jumlah Penyewaan per Cuaca")
fig, ax = plt.subplots()
sns.barplot(
    data=jam.groupby(by='weathersit')[['cnt']].sum()
    .reset_index()
    .melt(id_vars='weathersit', var_name='Cuaca', value_name='Jumlah'),
    x='weathersit',
    y='Jumlah',
    hue='Cuaca',
    palette={'cnt':'green'},
    ax=ax
)
ax.set_xlabel('Cuaca')
ax.set_ylabel('Total Penyewaan')
ax.set_title('Jumlah Penyewaan per Cuaca')
st.pyplot(fig)

st.write("Data terakhir diperbarui dari MainData.csv")

st.markdown("2025 | Dibuat oleh Putra Ade Nirada | Data dari BikeSharingDataset")

