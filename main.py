import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
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
    .prediction-card {
        background-color: #f7f7f7;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)

# Judul dengan styling
st.markdown("""
    <h1 style='text-align: center; color: #0066cc; margin-bottom: 2rem;'>
        📈 Prediksi Saham dengan Model STACN
    </h1>
    """, unsafe_allow_html=True)

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

# Layout dengan kolom
col1, col2 = st.columns([2, 1])

# PANEL PREDIKSI DI KIRI (Area lebih luas)
with col1:
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
            options=["1 Hari", "2 Hari", "3 Hari", "5 Hari", "10 Hari"],
            value="5 Hari"
        )
        
        submit_button = st.form_submit_button("Prediksi Harga Saham")
        
        if submit_button:
            with st.spinner('Melakukan prediksi...'):
                # Simulasi prediksi
                import time
                time.sleep(1)
                
                # Mendapatkan jumlah hari dari selection
                days = int(prediction_range.split()[0])
                last_price = df['Close'].iloc[-1]
                
                # Fungsi untuk menghasilkan prediksi yang realistis
                def generate_predictions(start_price, days, volatility=0.015):
                    prices = [start_price]
                    for i in range(days):
                        change = np.random.normal(0.002, volatility) 
                        new_price = prices[-1] * (1 + change)
                        prices.append(new_price)
                    return prices[1:]  # Skip start price
                
                predictions = generate_predictions(last_price, days)
                future_dates = [(date.today() + timedelta(days=i+1)).strftime('%d %b') for i in range(days)]
                
                st.success(f"Prediksi untuk {days} hari ke depan berhasil!")
                
                # Visualisasi prediksi
                pred_df = pd.DataFrame({
                    'Tanggal': future_dates,
                    'Prediksi': predictions
                })
                
                # Grafik prediksi - Tampilkan lebih dulu karena lebih penting
                hist_dates = df['Date'].iloc[-5:].tolist()
                hist_prices = df['Close'].iloc[-5:].tolist()
                
                all_dates = hist_dates + [datetime.strptime(f"{date.today().year} {d}", "%Y %d %b") for d in future_dates]
                all_prices = hist_prices + predictions
                
                fig2 = go.Figure()
                
                # Historical prices
                fig2.add_trace(go.Scatter(
                    x=hist_dates, 
                    y=hist_prices,
                    mode='lines',
                    name='Historis',
                    line=dict(color='#0066cc', width=2)
                ))
                
                # Predicted prices
                fig2.add_trace(go.Scatter(
                    x=[hist_dates[-1]] + [datetime.strptime(f"{date.today().year} {d}", "%Y %d %b") for d in future_dates],
                    y=[hist_prices[-1]] + predictions,
                    mode='lines+markers',
                    name='Prediksi',
                    line=dict(color='#FF9900', width=2, dash='dot'),
                    marker=dict(size=8)
                ))
                
                fig2.update_layout(
                    title='Prediksi Harga',
                    yaxis_title='Harga',
                    xaxis_title='Tanggal',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Tampilkan hasil prediksi detail di bawah chart
                st.markdown("##### Hasil Prediksi Detail:")
                prediction_cols = st.columns(min(3, days))
                
                for i, row in pred_df.iterrows():
                    col_idx = i % len(prediction_cols)
                    with prediction_cols[col_idx]:
                        change = ((row['Prediksi'] - last_price if i == 0 else 
                                row['Prediksi'] - pred_df.iloc[i-1]['Prediksi']) / 
                                (last_price if i == 0 else pred_df.iloc[i-1]['Prediksi'])) * 100
                        
                        change_color = "green" if change >= 0 else "red"
                        change_arrow = "↑" if change >= 0 else "↓"
                        
                        st.markdown(f"""
                        <div class="prediction-card">
                            <h6>{row['Tanggal']}</h6>
                            <p style="font-size: 1.2rem; font-weight: bold">${row['Prediksi']:.2f} 
                            <span style="color: {change_color};">{change_arrow} {abs(change):.2f}%</span></p>
                        </div>
                        """, unsafe_allow_html=True)

# PANEL ANALISIS HISTORIS DI KANAN
with col2:
    st.markdown("### 📊 Analisis Data Historis")
    
    # Metrics card
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Harga Terakhir", f"${df['Close'].iloc[-1]:.2f}", 
                 f"{((df['Close'].iloc[-1] - df['Close'].iloc[-2])/df['Close'].iloc[-2]*100):.2f}%")
    with metric_col2:
        st.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}", 
                 f"{((df['Volume'].iloc[-1] - df['Volume'].iloc[-2])/df['Volume'].iloc[-2]*100):.2f}%")
    
    # Interactive chart using Plotly Line Chart
    time_range = st.select_slider(
        "Rentang Waktu",
        options=["5 Hari", "10 Hari", "1 Bulan", "3 Bulan"],
        value="10 Hari"
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
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Data historis detail langsung di bawah chart
    st.markdown("##### Data Historis Detail")
    st.dataframe(
        filtered_df.style.format({
            'Open': '${:.2f}',
            'High': '${:.2f}',
            'Low': '${:.2f}',
            'Close': '${:.2f}',
            'Volume': '{:,.0f}'
        }),
        height=200
    )
