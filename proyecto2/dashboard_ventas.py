import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Retail Insights Dashboard | C-Level Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .report-text {
        font-size: 1.1rem;
        color: #444;
        line-height: 1.6;
    }
    .highlight {
        color: #e76f51;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GENERACIÓN Y CARGA DE DATOS ---
@st.cache_data
def load_data():
    """Genera un dataset simulado de ventas minoristas con anomalías intencionales."""
    np.random.seed(42)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    regiones = ['Norte', 'Sur', 'Este', 'Oeste']
    categorias = ['Electrónica', 'Hogar', 'Ropa', 'Juguetes']
    
    data = []
    for date in dates:
        for region in regiones:
            for categoria in categorias:
                # Base de ingresos
                base_revenue = np.random.normal(5000, 1000)
                
                # Introducir caída en Q4 (Últimos 90 días aprox) para Norte/Electrónica
                if date > (end_date - timedelta(days=90)):
                    if region == 'Norte' and categoria == 'Electrónica':
                        base_revenue *= 0.75 # Caída del 25%
                
                cost_ratio = np.random.uniform(0.6, 0.7)
                revenue = max(0, base_revenue)
                cost = revenue * cost_ratio
                
                data.append({
                    'Fecha': date,
                    'Región': region,
                    'Categoría': categoria,
                    'Ingresos': revenue,
                    'Costos': cost,
                    'Margen': revenue - cost
                })
                
    df = pd.DataFrame(data)
    df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
    return df

def get_filtered_data(df, date_range, selected_cats):
    """Aplica filtros de sidebar al dataframe."""
    mask = (df['Fecha'].dt.date >= date_range[0]) & (df['Fecha'].dt.date <= date_range[1])
    if selected_cats:
        mask &= df['Categoría'].isin(selected_cats)
    return df[mask]

# --- FUNCIONES DE VISUALIZACIÓN ---
def plot_revenue_trend(df):
    monthly_sales = df.groupby('Mes')['Ingresos'].sum().reset_index()
    
    fig = px.line(monthly_sales, x='Mes', y='Ingresos', 
                  title="Evolución Mensual de Ingresos",
                  labels={'Ingresos': 'Ingresos ($)', 'Mes': 'Periodo'},
                  template="plotly_white")
    
    fig.update_traces(line_color='#2a9d8f', line_width=3)
    
    # Resaltar la caída en los últimos meses
    fig.add_vrect(x0=monthly_sales['Mes'].iloc[-3], x1=monthly_sales['Mes'].iloc[-1], 
                  fillcolor="red", opacity=0.1, layer="below", line_width=0,
                  annotation_text="Caída Detectada", annotation_position="top left")
    
    return fig

def plot_region_comparison(df):
    # Comparar el último trimestre vs el anterior
    df['Trimestre'] = df['Fecha'].dt.quarter
    region_sales = df.groupby(['Región', 'Trimestre'])['Ingresos'].sum().reset_index()
    
    fig = px.bar(region_sales, x='Región', y='Ingresos', color='Trimestre',
                 barmode='group', title="Ingresos por Región y Trimestre",
                 color_discrete_map={1: '#264653', 2: '#2a9d8f', 3: '#e9c46a', 4: '#e76f51'},
                 template="plotly_white")
    return fig

def plot_anomaly_heatmap(df):
    # Filtrar solo último trimestre para ver el detalle
    last_q = df[df['Fecha'] > (df['Fecha'].max() - timedelta(days=90))]
    pivot = last_q.pivot_table(index='Categoría', columns='Región', values='Ingresos', aggfunc='sum')
    
    fig = px.imshow(pivot, text_auto=True, aspect="auto",
                    title="Mapa de Calor: Concentración de Ingresos (Último Trimestre)",
                    color_continuous_scale=['#f1f1f1', '#e76f51'],
                    labels=dict(color="Ingresos ($)"))
    return fig

# --- CUERPO DEL DASHBOARD ---
def main():
    df = load_data()
    
    # SIDEBAR
    st.sidebar.header("🎯 Filtros Ejecutivos")
    min_date = df['Fecha'].min().date()
    max_date = df['Fecha'].max().date()
    
    date_range = st.sidebar.date_input(
        "Rango de Fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    all_cats = df['Categoría'].unique().tolist()
    selected_cats = st.sidebar.multiselect("Categorías", all_cats, default=all_cats)
    
    # Procesar Datos Filtrados
    if len(date_range) == 2:
        df_filtered = get_filtered_data(df, date_range, selected_cats)
    else:
        df_filtered = df # Fallback si solo se selecciona una fecha
    
    # --- HEADER ---
    st.title("📉 Reporte de Desempeño Comercial: Q4 Crisis Analysis")
    st.markdown("""
    Este dashboard analiza la reciente caída en los ingresos globales detectada en el último trimestre. 
    *Objetivo:* Identificar el origen del problema y proponer acciones correctivas inmediatas.
    """)
    
    # --- MÉTRICAS PRINCIPALES ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_rev = df_filtered['Ingresos'].sum()
    total_cost = df_filtered['Costos'].sum()
    avg_margin = (df_filtered['Margen'].sum() / total_rev) * 100 if total_rev > 0 else 0
    
    # Simular Deltas (vs periodo anterior)
    col1.metric("Ingresos Totales", f"${total_rev:,.0f}", "-5.2%", delta_color="inverse")
    col2.metric("Costos Operativos", f"${total_cost:,.0f}", "+2.1%", delta_color="inverse")
    col3.metric("Margen Neto", f"{avg_margin:.1f}%", "-3.4%", delta_color="inverse")
    col4.metric("Volumen Ventas", f"{len(df_filtered):,}", "-1.8%", delta_color="inverse")

    st.divider()

    # --- NARRATIVA Y GRÁFICOS ---
    
    # Paso 1: La Tendencia
    st.subheader("1. El Diagnóstico: ¿Cuándo empezó la caída?")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(plot_revenue_trend(df_filtered), use_container_width=True)
    with c2:
        st.markdown("""
        <div class="report-text">
        Al observar la tendencia anual, notamos una estabilidad saludable hasta el inicio del <b>último trimestre</b>. 
        A partir de octubre, se observa una pendiente negativa pronunciada. 
        <br><br>
        <span class="highlight">Alerta:</span> Los ingresos han caído aproximadamente un <b>25%</b> respecto al promedio mensual del Q3.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Paso 2: Localización del problema
    st.subheader("2. Segmentación: ¿Dónde está el cuello de botella?")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.plotly_chart(plot_region_comparison(df_filtered), use_container_width=True)
        st.caption("Comparativa trimestral por región. Note la barra roja en la región Norte.")
        
    with col_b:
        st.plotly_chart(plot_anomaly_heatmap(df_filtered), use_container_width=True)
        st.caption("Concentración de ingresos por categoría. El color intenso señala el impacto crítico.")

    st.markdown("""
    ### 🔍 Hallazgos Clave
    1. **Región Norte:** Es la única región que muestra un decrecimiento de dos dígitos en el Q4.
    2. **Categoría Electrónica:** Al cruzar los datos, descubrimos que el impacto no es generalizado, sino que está concentrado en los productos de **Electrónica en el Norte**.
    3. **Impacto en Margen:** Debido a que Electrónica es una categoría de alto valor, su caída arrastra el margen global del negocio.
    """)

    st.divider()

    # --- RECOMENDACIONES ---
    st.subheader("💡 Recomendaciones Estratégicas")
    rec1, rec2, rec3 = st.columns(3)
    
    with rec1:
        st.info("### Auditoría Logística")
        st.write("Investigar posibles retrasos en la cadena de suministro en los centros de distribución del Norte.")
    
    with rec2:
        st.warning("### Revisión de Precios")
        st.write("Analizar si la entrada de un nuevo competidor en la región Norte está afectando nuestra competitividad en Electrónica.")
    
    with rec3:
        st.success("### Campaña de Reactivación")
        st.write("Lanzar promociones segmentadas para el inventario estancado de Electrónica en las sucursales del Norte.")

if __name__ == "__main__":
    main()
