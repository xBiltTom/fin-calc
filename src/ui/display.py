import streamlit as st
from config.constants import MONEDA


def mostrar_resumen_inversion(datos: dict):
    """
    Muestra un resumen de los datos de inversión ingresados.
    
    Args:
        datos: Diccionario con los datos de inversión
    """
    st.subheader("📋 Resumen de Inversión")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Inversión Inicial",
            value=f"{MONEDA} {datos['valor_presente']:,.2f}"
        )
    
    with col2:
        st.metric(
            label=f"Aporte {datos['frecuencia']}",
            value=f"{MONEDA} {datos['aporte_periodico']:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Plazo",
            value=f"{datos['plazo_años']} años"
        )
    
    with col4:
        st.metric(
            label="TEA",
            value=f"{datos['tea_pct']:.2f}%"
        )


def mostrar_resultados_vf(vf: float, inversion_total: float, beneficio_bruto: float):
    """
    Muestra los resultados del cálculo de valor futuro.
    
    Args:
        vf: Valor Futuro
        inversion_total: Inversión total realizada
        beneficio_bruto: Beneficio bruto (sin impuestos)
    """
    st.subheader("💰 Valor Futuro de la Inversión")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Valor Futuro (VF)",
            value=f"{MONEDA} {vf:,.2f}",
            delta=f"+{MONEDA} {beneficio_bruto:,.2f}",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Inversión Total",
            value=f"{MONEDA} {inversion_total:,.2f}"
        )
    
    with col3:
        rentabilidad_pct = (beneficio_bruto / inversion_total * 100) if inversion_total > 0 else 0
        st.metric(
            label="Rentabilidad",
            value=f"{rentabilidad_pct:.2f}%"
        )


def mostrar_resultados_retiro_total(
    vf: float,
    beneficio_bruto: float,
    impuesto: float,
    monto_neto: float,
    tipo_bolsa: str
):
    """
    Muestra los resultados de un retiro total.
    
    Args:
        vf: Valor Futuro
        beneficio_bruto: Beneficio bruto
        impuesto: Monto de impuesto
        monto_neto: Monto neto después de impuestos
        tipo_bolsa: Tipo de inversión (Nacional/Extranjera)
    """
    st.subheader("🏦 Retiro Total")
    
    tasa_impuesto = "5%" if tipo_bolsa == "Nacional" else "29.5%"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Valor Futuro",
            value=f"{MONEDA} {vf:,.2f}"
        )
    
    with col2:
        st.metric(
            label=f"Impuesto ({tasa_impuesto})",
            value=f"{MONEDA} {impuesto:,.2f}",
            delta=f"-{MONEDA} {impuesto:,.2f}",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Monto Neto a Recibir",
            value=f"{MONEDA} {monto_neto:,.2f}",
            delta=f"Después de impuestos",
            delta_color="off"
        )
    
    st.info(f"💡 Se aplicó un impuesto del **{tasa_impuesto}** sobre la ganancia de {MONEDA} {beneficio_bruto:,.2f}")


def mostrar_resultados_retiro_mensual(
    retiro_mensual: float,
    meses: int,
    total_retirado: float,
    vf: float
):
    """
    Muestra los resultados de retiros mensuales.
    
    Args:
        retiro_mensual: Monto de retiro mensual
        meses: Número de meses de retiro
        total_retirado: Total que se retirará
        vf: Valor Futuro original
    """
    st.subheader("💳 Retiros Mensuales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Retiro Mensual",
            value=f"{MONEDA} {retiro_mensual:,.2f}"
        )
    
    with col2:
        st.metric(
            label="Durante",
            value=f"{meses} meses ({meses/12:.1f} años)"
        )
    
    with col3:
        st.metric(
            label="Total a Retirar",
            value=f"{MONEDA} {total_retirado:,.2f}"
        )
    
    st.info(f"💡 Se utilizará el valor futuro de {MONEDA} {vf:,.2f} para generar estos retiros mensuales")
