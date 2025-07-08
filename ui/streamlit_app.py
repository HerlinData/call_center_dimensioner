"""
Aplicación Streamlit - Dimensionador Call Center
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date, timedelta
import sys
from pathlib import Path
import logging

# Configurar página
st.set_page_config(
    page_title="Dimensionador Call Center",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Agregar path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Configurar logging
logging.basicConfig(level=logging.ERROR)  # Solo errores en Streamlit

# CSS personalizado con colores corporativos
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #da7756 0%, #c2563a 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #da7756;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .scenario-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 2px solid #da7756;
    }
    
    .recommendation-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    /* Sidebar BALANCEADO */
    .css-1d391kg {
        padding: 1.5rem 1rem !important;
        background: #ffffff !important;
    }
    
    /* Espaciado balanceado entre secciones */
    .stMarkdown h3, .stMarkdown h2 {
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox, .stDateInput {
        margin-bottom: 0.5rem !important;
    }
    
    /* TODOS los botones - base */
    .stButton > button {
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        margin: 10px 0 !important;
        min-height: 44px !important;
        width: 100% !important;
        color: white !important;
    }
    
    /* PRIMARY = AZUL */
    .stButton > button[kind="primary"] {
        background: #2196f3 !important;
        box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3) !important;
    }
    
    /* Verde para botón intermedio - selector directo */
    .stButton > button:contains("Intermedio") {
        background-color: #4caf50 !important;
        color: white !important;
    }
    
    /* Morado para botón avanzado - selector directo */
    .stButton > button:contains("Avanzado") {
        background-color: #9c27b0 !important;
        color: white !important;
    }
    
    
    /* Inputs limpios y compactos */
    .stSelectbox > div > div, .stDateInput > div > div > div {
        border-radius: 4px !important;
        border: 1px solid #dee2e6 !important;
        font-size: 14px !important;
    }
    
    /* Métricas compactas */
    .stMetric {
        background: #f8f9fa !important;
        padding: 8px !important;
        border-radius: 4px !important;
        border-left: 3px solid #da7756 !important;
    }
</style>
""", unsafe_allow_html=True)

# Imports de módulos propios
try:
    from config.auth import auth_manager
    from data.sql_connector import sql_connector
    from data.data_analyzer import data_analyzer
    from engines.erlang_calculator import ErlangInputs
except ImportError as e:
    st.error(f"❌ Error importando módulos: {e}")
    st.stop()

def show_login():
    """Mostrar pantalla de login minimalista"""
    
    # Espaciado superior
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Layout centrado
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Header con estilo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #da7756; margin-bottom: 0.5rem;">AMG</h1>
            <p style="color: #6b7280; margin-bottom: 2rem;">Sistema de dimensionamiento</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulario simple
        with st.form("login_form", clear_on_submit=False):
            password = st.text_input(
                "Clave de acceso",
                type="password", 
                placeholder="Ingresa tu clave de acceso"
            )
            
            submitted = st.form_submit_button(
                "🔓 Ingresar", 
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if auth_manager.authenticate(password):
                    st.success("✅ Acceso concedido")
                    st.rerun()
                else:
                    st.error("❌ Clave incorrecta")
        
        # Información mínima
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: #9ca3af; font-size: 0.9rem;">
            Sistema para operaciones Telecom
        </div>
        """, unsafe_allow_html=True)

def show_nueva_campana_app():
    """Dashboard para dimensionamiento de campaña nueva"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Dimensionador - Campaña Nueva</h1>
        <p>Cálculo de staffing para nueva operación</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegación y logout en sidebar
    show_sidebar_navigation()
    
    # Contenido principal - placeholder por ahora
    st.markdown("## 🔧 En Construcción")
    st.info("Esta funcionalidad será implementada próximamente. Aquí podrás dimensionar campañas nuevas con inputs manuales.")
    
    st.markdown("""
    ### 📋 Funcionalidades Planificadas:
    - **Inputs manuales** de volumen esperado y TMO
    - **Cálculos Erlang C** para dimensionamiento básico
    - **Escenarios múltiples** (optimista, conservador, realista)
    - **Recomendaciones** basadas en mejores prácticas
    - **Exportación** de resultados
    """)

def show_analysis_selection():
    """Pantalla de selección de tipo de análisis"""
    
    
    # Header principal compacto
    modo_actual = st.session_state.get('modo_operacion', 'existente')
    tipo_campana = "Campaña Existente" if modo_actual == 'existente' else "Campaña Nueva"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #da7756 0%, #c2563a 100%); padding: 0.8rem; 
                border-radius: 10px; margin-bottom: 0.8rem; color: white; text-align: center;">
        <h2 style="margin: 0; margin-bottom: 0; font-size: 1.8rem; line-height: 1.1;">🎯 Selecciona el Tipo de Análisis</h2>
        <p style="margin: 0; margin-top: 0; font-size: 0.9rem; line-height: 1.2;">Para tu {tipo_campana}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout horizontal de selección - 3 columnas
    col1, col2, col3 = st.columns(3)
    
    # Opción 1: Análisis Básico
    with col1:
        st.markdown("""
        <div style="border: 2px solid #2196f3; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; 
                    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%); text-align: center; min-height: 180px;">
            <h3 style="color: #2196f3; margin: 0; margin-bottom: 0.8rem; font-size: 1.2rem;">⚡ Análisis Básico</h3>
            <p style="color: #6b7280; margin: 0; margin-bottom: 0.8rem; font-size: 0.95rem; line-height: 1.3;">
                Dimensionamiento rápido con Erlang C
            </p>
            <div style="background: #e3f2fd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem; text-align: left;">
                <strong style="color: #1976d2;">⚡ Características:</strong><br>
                • Cálculos instantáneos (< 1 seg)<br>
                • Dimensionamiento preciso<br>
                • Resultados inmediatos<br>
                • Ideal para análisis rápido
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "⚡ Usar Análisis Básico", 
            type="primary", 
            use_container_width=True,
            key="btn_basico"
        ):
            st.session_state['tipo_analisis'] = 'basico'
            st.session_state['analisis_seleccionado'] = True
            st.rerun()
    
    # Opción 2: Análisis Intermedio
    with col2:
        st.markdown("""
        <div style="border: 2px solid #4caf50; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; 
                    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%); text-align: center; min-height: 180px;">
            <h3 style="color: #4caf50; margin: 0; margin-bottom: 0.8rem; font-size: 1.2rem;">📊 Análisis Intermedio</h3>
            <p style="color: #6b7280; margin: 0; margin-bottom: 0.8rem; font-size: 0.95rem; line-height: 1.3;">
                Simulación con abandonos incluidos
            </p>
            <div style="background: #e8f5e8; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem; text-align: left;">
                <strong style="color: #388e3c;">📊 Características:</strong><br>
                • Simulaciones con SimPy<br>
                • Incluye abandonos de llamadas<br>
                • Análisis más realista<br>
                • Tiempo: 2-5 segundos
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
        
        # Botón HTML directo - VERDE
        intermedio_clicked = st.markdown("""
        <form action="" method="get">
            <button type="submit" name="btn_intermedio" value="true" 
                    style="background-color: #4caf50; color: white; border: none; 
                           border-radius: 8px; padding: 12px 24px; font-weight: 600; 
                           width: 100%; cursor: pointer; font-size: 14px;">
                📊 Usar Análisis Intermedio
            </button>
        </form>
        """, unsafe_allow_html=True)
        
        # Detectar si se hizo clic
        if st.query_params.get("btn_intermedio") == "true":
            st.session_state['tipo_analisis'] = 'intermedio'
            st.session_state['analisis_seleccionado'] = True
            st.query_params.clear()
            st.rerun()
    
    # Opción 3: Análisis Avanzado
    with col3:
        st.markdown("""
        <div style="border: 2px solid #9c27b0; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; 
                    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%); text-align: center; min-height: 180px;">
            <h3 style="color: #9c27b0; margin: 0; margin-bottom: 0.8rem; font-size: 1.2rem;">🔬 Análisis Avanzado</h3>
            <p style="color: #6b7280; margin: 0; margin-bottom: 0.8rem; font-size: 0.95rem; line-height: 1.3;">
                Shrinkage + validación automática
            </p>
            <div style="background: #f3e5f5; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem; text-align: left;">
                <strong style="color: #7b1fa2;">🔬 Características:</strong><br>
                • Validación automática<br>
                • Incluye shrinkage detallado<br>
                • Múltiples escenarios<br>
                • Análisis más completo
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
        # Botón HTML directo - MORADO
        avanzado_clicked = st.markdown("""
        <form action="" method="get">
            <button type="submit" name="btn_avanzado" value="true" 
                    style="background-color: #9c27b0; color: white; border: none; 
                           border-radius: 8px; padding: 12px 24px; font-weight: 600; 
                           width: 100%; cursor: pointer; font-size: 14px;">
                🔬 Usar Análisis Avanzado
            </button>
        </form>
        """, unsafe_allow_html=True)
        
        # Detectar si se hizo clic
        if st.query_params.get("btn_avanzado") == "true":
            st.session_state['tipo_analisis'] = 'avanzado'
            st.session_state['analisis_seleccionado'] = True
            st.query_params.clear()
            st.rerun()
    
    # Sidebar con navegación
    with st.sidebar:
        st.markdown("### 📋 Configuración Actual")
        st.info(f"🎯 {tipo_campana}")
        
        st.markdown("---")
        
        # Botón para volver a selección de campaña
        if st.button("⬅️ Cambiar Tipo", use_container_width=True):
            st.session_state['modo_seleccionado'] = False
            if 'modo_operacion' in st.session_state:
                del st.session_state['modo_operacion']
            st.rerun()
        
        # Botón logout
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            # Limpiar todas las variables de sesión
            for key in ['modo_operacion', 'modo_seleccionado', 'tipo_analisis', 'analisis_seleccionado']:
                if key in st.session_state:
                    del st.session_state[key]
            auth_manager.logout()
            st.rerun()

def show_sidebar_navigation():
    """Sidebar con navegación común"""
    with st.sidebar:
        st.markdown("### 📋 Configuración Actual")
        
        modo_actual = st.session_state.get('modo_operacion', 'existente')
        tipo_analisis = st.session_state.get('tipo_analisis', 'basico')
        
        if modo_actual == 'existente':
            st.info("🎯 Campaña Existente")
        else:
            st.info("🎯 Campaña Nueva")
        
        # Mostrar tipo de análisis
        analisis_nombres = {
            'basico': '⚡ Básico (Erlang C)',
            'intermedio': '📊 Intermedio (SimPy)',
            'avanzado': '🔬 Avanzado (SimPy)'
        }
        st.success(f"📋 {analisis_nombres.get(tipo_analisis, 'Básico')}")
        
        st.markdown("---")
        
        # Botón para cambiar análisis
        if st.button("🔄 Cambiar Análisis", use_container_width=True):
            st.session_state['analisis_seleccionado'] = False
            if 'tipo_analisis' in st.session_state:
                del st.session_state['tipo_analisis']
            st.rerun()
        
        # Botón para cambiar campaña
        if st.button("⬅️ Cambiar Tipo", use_container_width=True):
            st.session_state['modo_seleccionado'] = False
            st.session_state['analisis_seleccionado'] = False
            for key in ['modo_operacion', 'tipo_analisis']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Botón logout
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            # Limpiar todas las variables de sesión
            for key in ['modo_operacion', 'modo_seleccionado', 'tipo_analisis', 'analisis_seleccionado']:
                if key in st.session_state:
                    del st.session_state[key]
            auth_manager.logout()
            st.rerun()

def show_main_app():
    """Mostrar aplicación principal para campaña existente"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dimensionador - Datos Históricos</h1>
        <p>Análisis inteligente basado en datos reales de SQL Server</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegación y logout en sidebar
    show_sidebar_navigation()
    
    # Sidebar MINIMALISTA - REDISEÑO COMPLETO
    with st.sidebar:
        # Obtener rango de fechas disponibles
        try:
            with st.spinner("⏳"):
                date_range = sql_connector.get_available_date_range()
                min_date = date_range['fecha_min']
                max_date = date_range['fecha_max']
                
        except Exception as e:
            st.error(f"❌ {e}")
            st.stop()
        
        # HEADER COMPACTO
        st.markdown("## 📊 Dimensionador")
        
        # FECHAS - COMPACTAS EN 2 COLUMNAS
        st.markdown("**📅 Período de Análisis**")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Inicio", value=min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("Fin", value=max_date, min_value=min_date, max_value=max_date)
        
        if start_date > end_date:
            st.error("❌ Fechas inválidas")
            st.stop()
        
        # PARÁMETROS - COMPACTOS EN 2 COLUMNAS
        st.markdown("**🎯 Parámetros SLA**")
        col1, col2 = st.columns(2)
        with col1:
            sla_target = st.selectbox("SLA %", [80, 85, 90, 95], index=2)
        with col2:
            answer_time_target = st.selectbox("Tiempo (s)", [15, 20, 25, 30], index=1)
        
        # SHRINKAGE - UNA LÍNEA
        shrinkage_pct = st.selectbox("⚙️ Shrinkage (%)", [10, 15, 20, 25], index=1)
        
        # BOTÓN PRINCIPAL 
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button(
            "🚀 Ejecutar Análisis",
            type="primary",
            use_container_width=True
        )
        
        # INFO COMPACTA
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Registros", f"{date_range['total_registros']:,}")
        with col2:
            st.metric("👥 Asesores", date_range['total_asesores'])
        
        st.caption(f"📅 Rango: {min_date} → {max_date}")
    
    # Contenido principal
    if analyze_btn:
        execute_analysis(start_date, end_date, sla_target, answer_time_target, shrinkage_pct)
    else:
        show_welcome_screen(date_range if 'date_range' in locals() else None)

def show_welcome_screen(date_range):
    """Pantalla de bienvenida"""
    
    st.markdown("## 👋 Bienvenido al Dimensionador Call Center")
    
    if date_range:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📞 Total Registros</h3>
                <h2>{:,}</h2>
            </div>
            """.format(date_range['total_registros']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>👥 Total Asesores</h3>
                <h2>{}</h2>
            </div>
            """.format(date_range['total_asesores']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📅 Fecha Inicio</h3>
                <h2>{}</h2>
            </div>
            """.format(date_range['fecha_min']), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>📅 Fecha Fin</h3>
                <h2>{}</h2>
            </div>
            """.format(date_range['fecha_max']), unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Cómo usar el sistema:
    
    1. **📅 Selecciona el período** de análisis en el panel izquierdo
    2. **⚙️ Ajusta los parámetros** de SLA y shrinkage según tus necesidades
    3. **🚀 Ejecuta el análisis** para obtener dimensionamiento basado en datos reales
    4. **📊 Revisa los resultados** y escenarios recomendados
    5. **📄 Exporta los reportes** en Excel para presentaciones
    
    ### ✨ Características principales:
    
    - **Análisis en tiempo real** con datos de SQL Server
    - **Múltiples escenarios** de dimensionamiento (promedio, pico, conservador, optimista)
    - **Validación automática** contra datos históricos reales
    - **Recomendaciones inteligentes** basadas en análisis estadístico
    - **Exportación a Excel** con gráficos integrados
    """)

def execute_analysis(start_date, end_date, sla_target, answer_time_target, shrinkage_pct):
    """Ejecutar análisis completo"""
    
    st.markdown("## 🔍 Ejecutando Análisis...")
    
    # Barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Paso 1: Obtener datos
        status_text.text("📊 Obteniendo datos históricos...")
        progress_bar.progress(20)
        
        # Ejecutar análisis completo
        with st.spinner("Procesando análisis completo..."):
            results = data_analyzer.analyze_campaign_complete(
                start_date=start_date,
                end_date=end_date,
                sla_target=sla_target / 100,  # Convertir a decimal
                answer_time_target=answer_time_target,
                shrinkage_pct=shrinkage_pct
            )
        
        progress_bar.progress(100)
        status_text.text("✅ Análisis completado exitosamente")
        
        # Mostrar resultados
        show_results(results)
        
    except Exception as e:
        st.error(f"❌ Error en el análisis: {e}")
        st.exception(e)

def show_results(results):
    """Mostrar resultados del análisis"""
    
    st.markdown("## 📊 Resultados del Análisis")
    
    # Resumen ejecutivo
    summary = results['summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Agentes Recomendados",
            summary['agentes_recomendados'],
            delta=f"vs {summary['agentes_actuales_promedio']:.0f} actuales"
        )
    
    with col2:
        st.metric(
            "🎯 Escenario Base",
            summary['escenario_base'].upper(),
            delta=f"{summary['precision_modelo']:.1f}% precisión"
        )
    
    with col3:
        st.metric(
            "📈 SLA Actual Estimado",
            f"{summary['sla_actual_estimado']:.1f}%",
            delta=f"vs {results['targets']['sla_target']:.0f}% objetivo"
        )
    
    with col4:
        st.metric(
            "⏳ TME Promedio Real",
            f"{summary['tme_promedio_real']:.1f}s",
            delta=f"vs {results['targets']['answer_time_target']}s objetivo"
        )
    
    # Tabs para organizar resultados
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Escenarios", "📈 Gráficos", "💡 Recomendaciones", "📄 Exportar"])
    
    with tab1:
        show_scenarios_tab(results)
    
    with tab2:
        show_charts_tab(results)
    
    with tab3:
        show_recommendations_tab(results)
    
    with tab4:
        show_export_tab(results)

def show_scenarios_tab(results):
    """Tab de escenarios de dimensionamiento"""
    
    st.markdown("### 🎯 Escenarios de Dimensionamiento Calculados")
    
    scenarios = results['dimensioning_results']['scenarios']
    
    cols = st.columns(2)
    
    for i, (scenario_name, scenario_data) in enumerate(scenarios.items()):
        col = cols[i % 2]
        
        with col:
            # Determinar color basado en recomendación
            is_recommended = scenario_name == results['summary']['escenario_base']
            border_color = "#da7756" if is_recommended else "#e9ecef"
            
            st.markdown(f"""
            <div style="border: 2px solid {border_color}; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; background: white;">
                <h4 style="color: #da7756; margin-bottom: 1rem;">
                    {scenario_name.upper()} {'⭐ RECOMENDADO' if is_recommended else ''}
                </h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                    <div><strong>👥 Agentes:</strong> {scenario_data['agents_with_shrinkage']}</div>
                    <div><strong>📈 Utilización:</strong> {scenario_data['utilization']:.1f}%</div>
                    <div><strong>🎯 Nivel Servicio:</strong> {scenario_data['service_level']:.1f}%</div>
                    <div><strong>⏱️ Tiempo Espera:</strong> {scenario_data['average_wait_time']:.1f}s</div>
                    <div><strong>📊 Prob. Esperar:</strong> {scenario_data['probability_of_wait']:.1f}%</div>
                    <div><strong>🔥 Intensidad:</strong> {scenario_data['traffic_intensity']:.1f} Erlangs</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabla comparativa
    st.markdown("### 📊 Comparación de Escenarios")
    
    df_scenarios = pd.DataFrame([
        {
            'Escenario': name.upper(),
            'Agentes con Shrinkage': data['agents_with_shrinkage'],
            'Nivel de Servicio (%)': data['service_level'],
            'Tiempo Espera (s)': data['average_wait_time'],
            'Utilización (%)': data['utilization'],
            'Probabilidad Esperar (%)': data['probability_of_wait']
        }
        for name, data in scenarios.items()
    ])
    
    # Destacar escenario recomendado
    def highlight_recommended(row):
        if row['Escenario'].lower() == results['summary']['escenario_base'].upper():
            return ['background-color: #fff3cd'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        df_scenarios.style.apply(highlight_recommended, axis=1),
        use_container_width=True
    )

def show_charts_tab(results):
    """Tab de gráficos y visualizaciones"""
    
    st.markdown("### 📈 Análisis Visual")
    
    # Gráfico de escenarios
    scenarios = results['dimensioning_results']['scenarios']
    
    # Preparar datos para gráfico
    scenario_names = list(scenarios.keys())
    agents_required = [data['agents_with_shrinkage'] for data in scenarios.values()]
    service_levels = [data['service_level'] for data in scenarios.values()]
    wait_times = [data['average_wait_time'] for data in scenarios.values()]
    
    # Gráfico de barras - Agentes por escenario
    fig1 = go.Figure(data=[
        go.Bar(
            x=scenario_names,
            y=agents_required,
            text=agents_required,
            textposition='auto',
            marker_color='#da7756'
        )
    ])
    
    fig1.update_layout(
        title="👥 Agentes Requeridos por Escenario",
        xaxis_title="Escenario",
        yaxis_title="Número de Agentes",
        showlegend=False
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico de dispersión - SLA vs Tiempo de Espera
    fig2 = go.Figure(data=[
        go.Scatter(
            x=wait_times,
            y=service_levels,
            mode='markers+text',
            text=scenario_names,
            textposition="top center",
            marker=dict(
                size=agents_required,
                sizemode='diameter',
                sizeref=max(agents_required)/50,
                color='#da7756',
                opacity=0.7
            )
        )
    ])
    
    fig2.update_layout(
        title="🎯 Nivel de Servicio vs Tiempo de Espera",
        xaxis_title="Tiempo de Espera (segundos)",
        yaxis_title="Nivel de Servicio (%)",
        showlegend=False
    )
    
    # Línea objetivo de SLA
    fig2.add_hline(
        y=results['targets']['sla_target'],
        line_dash="dash",
        line_color="red",
        annotation_text=f"SLA Objetivo: {results['targets']['sla_target']:.0f}%"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Patrones históricos si están disponibles
    if 'historical_analysis' in results:
        historical = results['historical_analysis']
        
        if 'hourly_profile' in historical['volume_analysis']:
            hourly_data = historical['volume_analysis']['hourly_profile']
            
            hours = list(hourly_data.keys())
            volumes = list(hourly_data.values())
            
            fig3 = go.Figure(data=[
                go.Bar(
                    x=hours,
                    y=volumes,
                    marker_color='#da7756'
                )
            ])
            
            fig3.update_layout(
                title="📊 Perfil de Volumen por Hora",
                xaxis_title="Hora del Día",
                yaxis_title="Número de Llamadas",
                showlegend=False
            )
            
            st.plotly_chart(fig3, use_container_width=True)

def show_recommendations_tab(results):
    """Tab de recomendaciones"""
    
    st.markdown("### 💡 Recomendaciones Inteligentes")
    
    recommendations = results.get('recommendations', {})
    
    # Recomendaciones de dimensionamiento
    if 'dimensionamiento' in recommendations:
        st.markdown("#### 🎯 Dimensionamiento")
        for rec in recommendations['dimensionamiento']:
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{rec['tipo']}:</strong> {rec['descripcion']}<br>
                <em>{rec.get('justificacion', '')}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # Recomendaciones operacionales
    if 'operacional' in recommendations:
        st.markdown("#### ⚙️ Operacionales")
        for rec in recommendations['operacional']:
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{rec['tipo']}:</strong> {rec['descripcion']}<br>
                <em>{rec.get('detalle', '')}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # Oportunidades de mejora
    if 'mejoras' in recommendations:
        st.markdown("#### 🚀 Oportunidades de Mejora")
        for rec in recommendations['mejoras']:
            st.markdown(f"""
            <div class="recommendation-box">
                <strong>{rec['tipo']}:</strong> {rec['descripcion']}<br>
                <em>{rec.get('sugerencia', '')}</em>
            </div>
            """, unsafe_allow_html=True)
    
    # Análisis de precisión
    if 'validation_results' in results:
        validation = results['validation_results']
        best_scenario = validation.get('best_scenario', {})
        
        if best_scenario:
            st.markdown("#### ✅ Validación del Modelo")
            
            precision = best_scenario.get('precision_tme', 0)
            
            if precision > 80:
                status_class = "status-success"
                status_text = "Excelente precisión del modelo"
            elif precision > 60:
                status_class = "status-warning"  
                status_text = "Precisión aceptable del modelo"
            else:
                status_class = "status-warning"
                status_text = "Modelo requiere calibración"
            
            st.markdown(f"""
            <div class="{status_class}">
                <strong>{status_text}:</strong> {precision:.1f}% de precisión en predicción de tiempos de espera
            </div>
            """, unsafe_allow_html=True)

def show_export_tab(results):
    """Tab de exportación"""
    
    st.markdown("### 📄 Exportar Resultados")
    
    st.markdown("""
    Genera un reporte completo en Excel con:
    - 📊 Resumen ejecutivo
    - 📈 Gráficos de escenarios
    - 💡 Recomendaciones detalladas
    - 📋 Datos de análisis
    - ✅ Justificaciones técnicas
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Exportar Reporte Completo", type="primary", use_container_width=True):
            # Aquí iría la lógica de exportación
            st.success("✅ Reporte generado exitosamente")
            st.download_button(
                label="⬇️ Descargar Excel",
                data="placeholder",  # Aquí iría el archivo Excel real
                file_name=f"dimensionamiento_call_center_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        if st.button("📋 Exportar Solo Datos", type="secondary", use_container_width=True):
            # Crear CSV con datos principales
            scenarios = results['dimensioning_results']['scenarios']
            df_export = pd.DataFrame([
                {
                    'Escenario': name,
                    'Agentes_Requeridos': data['agents_required'],
                    'Agentes_Con_Shrinkage': data['agents_with_shrinkage'],
                    'Nivel_Servicio_Pct': data['service_level'],
                    'Tiempo_Espera_Seg': data['average_wait_time'],
                    'Utilizacion_Pct': data['utilization'],
                    'Probabilidad_Esperar_Pct': data['probability_of_wait'],
                    'Intensidad_Trafico': data['traffic_intensity']
                }
                for name, data in scenarios.items()
            ])
            
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"escenarios_dimensionamiento_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

def show_mode_selection():
    """Pantalla de selección de modo de operación"""
    
    # Header principal compacto
    st.markdown("""
    <div style="background: linear-gradient(135deg, #da7756 0%, #c2563a 100%); padding: 0.8rem; 
                border-radius: 10px; margin-bottom: 0.8rem; color: white; text-align: center;">
        <h2 style="margin: 0; margin-bottom: 0; font-size: 2rem; line-height: 1.1;">🎯 Selecciona el Tipo de Análisis</h2>
        <p style="margin: 0; margin-top: 0; font-size: 1rem; line-height: 1.2;">Elige el modo de operación para tu dimensionamiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout horizontal de selección
    col1, col2 = st.columns(2)
    
    # Opción 1: Campaña Existente
    with col1:
        st.markdown("""
        <div style="border: 2px solid #da7756; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; 
                    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%); text-align: center; min-height: 180px;">
            <h3 style="color: #da7756; margin: 0; margin-bottom: 0.8rem; font-size: 1.2rem;">📊 Analizar Campaña Existente</h3>
            <p style="color: #6b7280; margin: 0; margin-bottom: 0.8rem; font-size: 0.95rem; line-height: 1.3;">
                Usa datos históricos de la base de datos para análisis precisos
            </p>
            <div style="background: #e3f2fd; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem; text-align: left;">
                <strong style="color: #1976d2;">✅ Incluye:</strong><br>
                • Análisis de datos históricos reales<br>
                • Validación automática de modelos<br>
                • Múltiples escenarios basados en patrones<br>
                • Comparación predicho vs real
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "📊 Usar Datos Históricos", 
            type="primary", 
            use_container_width=True,
            key="btn_existente"
        ):
            st.session_state['modo_operacion'] = 'existente'
            st.session_state['modo_seleccionado'] = True
            st.rerun()
        
        # CSS para cambiar color después del botón
        st.markdown("""
        <style>
        button[data-testid="baseButton-primary"]:contains("Históricos") {
            background-color: #da7756 !important;
        }
        </style>
        <script>
        setTimeout(() => {
            const btns = document.querySelectorAll('button');
            btns.forEach(b => {
                if (b.textContent.includes('Históricos')) {
                    b.style.backgroundColor = '#da7756';
                    b.style.color = 'white';
                }
            });
        }, 10);
        </script>
        """, unsafe_allow_html=True)
    
    # Opción 2: Campaña Nueva
    with col2:
        st.markdown("""
        <div style="border: 2px solid #28a745; border-radius: 12px; padding: 1.2rem; margin-bottom: 0.8rem; 
                    background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%); text-align: center; min-height: 180px;">
            <h3 style="color: #28a745; margin: 0; margin-bottom: 0.8rem; font-size: 1.2rem;">🚀 Dimensionar Campaña Nueva</h3>
            <p style="color: #6b7280; margin: 0; margin-bottom: 0.8rem; font-size: 0.95rem; line-height: 1.3;">
                Dimensionamiento para una nueva campaña con parámetros estimados
            </p>
            <div style="background: #e8f5e8; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; font-size: 0.85rem; text-align: left;">
                <strong style="color: #2e7d32;">✅ Incluye:</strong><br>
                • Inputs manuales de volumen y TMO<br>
                • Cálculos basados en teoría Erlang<br>
                • Escenarios optimista/conservador<br>
                • Recomendaciones para operación nueva
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(
            "🚀 Nueva Campaña", 
            type="secondary", 
            use_container_width=True,
            key="btn_nueva"
        ):
            st.session_state['modo_operacion'] = 'nueva'
            st.session_state['modo_seleccionado'] = True
            st.rerun()
        
        # CSS para cambiar color después del botón
        st.markdown("""
        <script>
        setTimeout(() => {
            const btns = document.querySelectorAll('button');
            btns.forEach(b => {
                if (b.textContent.includes('Nueva Campaña')) {
                    b.style.backgroundColor = '#28a745';
                    b.style.color = 'white';
                }
            });
        }, 10);
        </script>
        """, unsafe_allow_html=True)
    
    # Sidebar con logout
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Usuario Autenticado")
        st.success("✅ Sesión activa")
        
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            # Limpiar todas las variables de sesión
            for key in ['modo_operacion', 'modo_seleccionado']:
                if key in st.session_state:
                    del st.session_state[key]
            auth_manager.logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
            <p><strong>Call Center Dimensioner</strong></p>
            <p>Sistema AMG v2.0</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Función principal con nuevo flujo"""
    
    # Verificar autenticación
    if not auth_manager.is_authenticated():
        show_login()
    else:
        # Verificar si se ha seleccionado modo de campaña
        if not st.session_state.get('modo_seleccionado', False):
            show_mode_selection()
        # Verificar si se ha seleccionado tipo de análisis
        elif not st.session_state.get('analisis_seleccionado', False):
            show_analysis_selection()
        else:
            # Mostrar dashboard según el modo y análisis seleccionado
            modo = st.session_state.get('modo_operacion', 'existente')
            analisis = st.session_state.get('tipo_analisis', 'basico')
            
            if modo == 'existente':
                show_main_app()
            elif modo == 'nueva':
                show_nueva_campana_app()
            else:
                # Fallback - volver a selección
                st.session_state['modo_seleccionado'] = False
                st.rerun()

if __name__ == "__main__":
    main()