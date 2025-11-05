import streamlit as st
from config.constants import FRECUENCIAS, MONEDA


def render_formulario_entrada():
    """
    Renderiza el formulario de entrada de datos del usuario.
    
    Returns:
        dict: Diccionario con todos los valores ingresados
    """
    st.header("📊 Datos de la Inversión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Información Personal")
        edad_actual = st.number_input(
            "Edad actual",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Tu edad actual en años"
        )
        
        st.subheader("Inversión Inicial")
        valor_presente = st.number_input(
            f"Monto inicial ({MONEDA})",
            min_value=0.0,
            value=0.0,
            step=100.0,
            format="%.2f",
            help="Capital inicial a invertir (opcional)"
        )
    
    with col2:
        st.subheader("Aportes Periódicos")
        aporte_periodico = st.number_input(
            f"Aporte periódico ({MONEDA})",
            min_value=0.0,
            value=0.0,
            step=50.0,
            format="%.2f",
            help="Monto que aportarás periódicamente (opcional)"
        )
        
        frecuencia = st.selectbox(
            "Frecuencia de aportes",
            options=list(FRECUENCIAS.keys()),
            index=0,
            help="¿Con qué frecuencia realizarás los aportes?"
        )
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Plazo de Inversión")
        
        tipo_plazo = st.radio(
            "Definir plazo por:",
            options=["Años", "Edad de jubilación"],
            horizontal=True
        )
        
        if tipo_plazo == "Años":
            plazo_años = st.number_input(
                "Plazo (años)",
                min_value=1,
                max_value=50,
                value=10,
                step=1,
                help="Tiempo que durará la inversión"
            )
        else:
            edad_jubilacion = st.number_input(
                "Edad de jubilación",
                min_value=edad_actual + 1,
                max_value=100,
                value=min(65, edad_actual + 35),
                step=1,
                help="Edad a la que planeas jubilarte"
            )
            plazo_años = edad_jubilacion - edad_actual
            st.info(f"⏱️ Plazo calculado: **{plazo_años} años**")
    
    with col4:
        st.subheader("Rentabilidad e Impuestos")
        
        tea_pct = st.number_input(
            "Tasa Efectiva Anual (TEA %)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            format="%.2f",
            help="Tasa de retorno anual esperada"
        )
        
        tipo_bolsa = st.selectbox(
            "Tipo de inversión",
            options=["Nacional", "Extranjera"],
            index=0,
            help="Nacional: 5% impuesto | Extranjera: 29.5% impuesto"
        )
        
        if tipo_bolsa == "Nacional":
            st.success("💚 Impuesto: 5%")
        else:
            st.warning("💛 Impuesto: 29.5%")
    
    return {
        "edad_actual": edad_actual,
        "valor_presente": valor_presente,
        "aporte_periodico": aporte_periodico,
        "frecuencia": frecuencia,
        "frecuencia_anual": FRECUENCIAS[frecuencia],
        "plazo_años": plazo_años,
        "tea": tea_pct / 100,  # Convertir a decimal
        "tea_pct": tea_pct,
        "tipo_bolsa": tipo_bolsa
    }
