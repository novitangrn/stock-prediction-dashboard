import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import date, datetime
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title='Stock Prediction Dashboard',
    page_icon='📈',
    layout='wide'
)

# Custom CSS untuk styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .main > div {
        padding: 2rem;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Judul dengan styling
st.markdown("""
    <h1 style='text-align: center; color: #0066cc; margin-bottom: 2rem;'>
        📈 Prediksi Saham dengan Model STACN
    </h1>
    """, unsafe_allow_html=True)

# Layout dengan kolom
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Analisis Data Historis")
    
    # Data historis dengan cache
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

    # Metrics card
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Harga Terakhir", f"${df['Close'].iloc[-1]:.2f}", 
                 f"{((df['Close'].iloc[-1] - df['Close'].iloc[-2])/df['Close'].iloc[-2]*100):.2f}%")
    with metric_col2:
        st.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}", 
                 f"{((df['Volume'].iloc[-1] - df['Volume'].iloc[-2])/df['Volume'].iloc[-2]*100):.2f}%")
    with metric_col3:
        st.metric("52-Week High", f"${df['High'].max():.2f}")

    # Interactive chart using Plotly Line Chart
    time_range = st.select_slider(
        "Rentang Waktu",
        options=["5 Hari", "10 Hari", "1 Bulan", "3 Bulan", "1 Tahun"],
        value="1 Bulan"
    )

    ranges = {
        "5 Hari": 5,
        "10 Hari": 10,
        "1 Bulan": 30,
        "3 Bulan": 90,
        "1 Tahun": 365
    }

    filtered_df = df.tail(ranges[time_range])
    
    fig = go.Figure()
    
    # Menambahkan line untuk setiap indikator
    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Close'],
                            mode='lines', name='Close',
                            line=dict(color='#0066cc', width=2)))
    
    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Open'],
                            mode='lines', name='Open',
                            line=dict(color='#00cc66', width=2)))
    
    fig.update_layout(
        title='Pergerakan Harga Saham',
        yaxis_title='Harga',
        xaxis_title='Tanggal',
        template='plotly_white',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📰 Input Berita & Prediksi")
    
    with st.form("prediction_form"):
        news_date = st.date_input("Tanggal Berita", value=date.today())
        
        st.markdown("##### Judul Berita Hari Ini")
        news_titles = st.text_area(
            "Masukkan 5 Judul Berita (Pisahkan dengan Enter)",
            height=150,
            placeholder="Contoh:\nBerita 1\nBerita 2\nBerita 3..."
        )
        
        prediction_range = st.select_slider(
            "Rentang Prediksi",
            options=["1 Hari", "2 Hari", "3 Hari", "5 Hari", "10 Hari", "15 Hari", "20 Hari"],
            value="5 Hari"
        )
        
        submit_button = st.form_submit_button("Prediksi Harga Saham")
        
        if submit_button:
            with st.spinner('Melakukan prediksi...'):
                # Simulasi prediksi
                import time
                time.sleep(1)
                prediction_result = 150.75
                
                st.success("Prediksi Berhasil!")
                st.metric(
                    "Prediksi Harga",
                    f"${prediction_result:.2f}",
                    f"+{((prediction_result - df['Close'].iloc[-1])/df['Close'].iloc[-1]*100):.2f}%"
                )

# Tabel data historis dengan styling
st.markdown("### 📋 Data Historis Detail")
st.dataframe(
    df.style.format({
        'Open': '${:.2f}',
        'High': '${:.2f}',
        'Low': '${:.2f}',
        'Close': '${:.2f}',
        'Volume': '{:,.0f}'
    }),
    height=300
)
