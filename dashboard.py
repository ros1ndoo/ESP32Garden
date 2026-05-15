import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Data Science Garden", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px 20px;
        border-radius: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #9da5b1 !important;
        font-size: 16px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Análisis de Datos: Estación IoT")
st.markdown("---")

st.sidebar.header("Configuración de Análisis")

try:
    df = pd.read_csv("datos_jardin.csv")
    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])

    min_date = df['fecha_hora'].min()
    max_date = df['fecha_hora'].max()
    
    rango = st.sidebar.slider(
        "Selecciona el rango de tiempo:",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="DD/MM HH:mm"
    )

    mask = (df['fecha_hora'] >= rango[0]) & (df['fecha_hora'] <= rango[1])
    df_filtrado = df.loc[mask]

    ultimo = df.iloc[-1]
    
    delta_suelo = None
    if len(df) > 1:
        delta_suelo = f"{ultimo['suelo'] - df.iloc[-2]['suelo']} %"

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperatura Actual", f"{ultimo['temperatura']} °C")
    with col2:
        st.metric("Humedad Ambiente", f"{ultimo['humedad_amb']} %")
    with col3:
        st.metric("Humedad Suelo", f"{ultimo['suelo']} %", delta=delta_suelo)
    with col4:
        st.metric("Muestras", len(df_filtrado))

    st.markdown("### Evolución Temporal Detallada")

    fig_temp = px.line(df_filtrado, x='fecha_hora', y='temperatura', 
                       title="Evolución de Temperatura",
                       line_shape="spline", render_mode="svg")
    fig_temp.update_traces(line_color='#FF4B4B')
    st.plotly_chart(fig_temp, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        fig_suelo = px.area(df_filtrado, x='fecha_hora', y='suelo', 
                            title="Humedad del Suelo (%)",
                            color_discrete_sequence=['#7D4F39'])
        st.plotly_chart(fig_suelo, use_container_width=True)
        
        st.write(f"**Media de humedad (Suelo):** {df_filtrado['suelo'].mean():.1f}%")

    with col_right:
        fig_hum_amb = px.area(df_filtrado, x='fecha_hora', y='humedad_amb', 
                              title="Humedad Ambiental (%)",
                              color_discrete_sequence=['#0077B6'])
        st.plotly_chart(fig_hum_amb, use_container_width=True)
        
        st.write(f"**Media de humedad (Ambiente):** {df_filtrado['humedad_amb'].mean():.1f}%")

    with st.expander("Ver registros completos (CSV)"):
        st.dataframe(df_filtrado.sort_values(by='fecha_hora', ascending=False))

except Exception as e:
    st.warning("Aún no hay datos suficientes. Asegúrate de que el script de captura se esté ejecutando.")
    st.info("Error detallado: " + str(e))

if st.button('Actualizar Datos'):
    st.rerun()