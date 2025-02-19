import streamlit as st
import pandas as pd
import math
from pathlib import Path
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(
    page_title='Stock Prediction Dashboard',
    page_icon=':stock:', # This is an emoji shortcode. Could be a URL too.
)

# Judul aplikasi
st.title("Prediksi Saham dengan Model STACN")

# Input tanggal berita
st.subheader("Masukkan Tanggal Berita")
news_date = st.date_input("Pilih Tanggal", value=date.today())

# Input judul berita
st.subheader("Masukkan Judul Berita Hari Ini")
news_titles = st.text_area("Masukkan 5 Judul Berita (Pisahkan dengan Enter)", height=150)
news_list = news_titles.split("\n") if news_titles else []


# Contoh data historis saham (kamu bisa mengganti ini dengan data asli)
@st.cache_data
def load_historical_data():
    dates = pd.date_range(end=date.today(), periods=365, freq='D')
    data = {
        "Date": dates,
        "Open": np.random.rand(365) * 100,
        "High": np.random.rand(365) * 100,
        "Low": np.random.rand(365) * 100,
        "Close": np.random.rand(365) * 100,
        "Volume": np.random.randint(1000, 10000, size=365),
        "Stock Num": np.random.randint(1, 100, size=365)
    }
    return pd.DataFrame(data)

df = load_historical_data()

# Pilih rentang waktu
st.subheader("Grafik Data Historis Saham")
time_range = st.selectbox("Pilih Rentang Waktu", ["5 Hari", "10 Hari", "1 Bulan", "1 Tahun"])

# Filter data berdasarkan rentang waktu
if time_range == "5 Hari":
    filtered_df = df.tail(5)
elif time_range == "10 Hari":
    filtered_df = df.tail(10)
elif time_range == "1 Bulan":
    filtered_df = df.tail(30)
else:
    filtered_df = df

# Pilih indikator
indicator = st.selectbox("Pilih Indikator", ["Open", "High", "Low", "Close"])

# Tampilkan grafik
st.line_chart(filtered_df.set_index("Date")[indicator])

st.subheader("Tabel Data Historis Saham")
st.dataframe(df)

st.subheader("Pilih Rentang Prediksi")
prediction_range = st.radio("Prediksi Harga untuk:", 
                            ["1 Hari ke Depan", "2 Hari ke Depan", "3 Hari ke Depan", 
                             "4 Hari ke Depan", "5 Hari ke Depan", "10 Hari ke Depan", 
                             "15 Hari ke Depan", "20 Hari ke Depan"])


st.subheader("Lakukan Prediksi")
if st.button("Prediksi Harga Saham"):
    # Panggil fungsi prediksi model STACN di sini
    # Contoh output sementara
    prediction_result = 150.75  # Ganti dengan hasil prediksi model
    st.success(f"Hasil Prediksi: {prediction_result}")

# Contoh grafik prediksi
st.subheader("Grafik Prediksi Harga Saham")
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4, 5], [100, 120, 130, 140, 150], marker='o')  # Contoh data prediksi
ax.set_xlabel("Hari ke Depan")
ax.set_ylabel("Harga Saham")
st.pyplot(fig)

# Tampilkan keterangan naik/turun/tetap
st.subheader("Keterangan Prediksi")
st.write("Harga saham diprediksi **naik** sebesar 5% dalam 5 hari ke depan.")
