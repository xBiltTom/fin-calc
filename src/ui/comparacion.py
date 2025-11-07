import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.calculations.financial_calcs import calcular_vf_combinado, calcular_beneficio_bruto
from src.calculations.tax_calcs import (
    calcular_impuesto_retiro_total,
    calcular_monto_neto_retiro_total,
    calcular_tasa_mensual_retiro,
    calcular_retiro_mensual_con_impuestos
)
from config.constants import MONEDA


def calcular_escenario(
    vp: float,
    aporte: float,
    tea: float,
    frecuencia_anual: int,
    plazo_años: int,
    tipo_bolsa: str,
    edad_actual: int,
    meses_retiro: int = 240,
    aporte_al_inicio: bool = False
) -> dict:
    """
    Calcula un escenario completo de inversión.
    
    Args:
        vp: Valor presente
        aporte: Aporte periódico
        tea: Tasa efectiva anual
        frecuencia_anual: Frecuencia de aportes
        plazo_años: Plazo en años
        tipo_bolsa: Nacional o Extranjera
        edad_actual: Edad actual del inversionista
        meses_retiro: Meses de retiro (default 240 = 20 años)
        aporte_al_inicio: True si el aporte es al inicio del periodo
    
    Returns:
        Diccionario con todos los cálculos del escenario
    """
    # Calcular VF
    vf = calcular_vf_combinado(vp, aporte, tea, frecuencia_anual, plazo_años, aporte_al_inicio)
    
    # Calcular inversión total y beneficio
    total_aportes = aporte * frecuencia_anual * plazo_años
    inversion_total = vp + total_aportes
    beneficio_bruto = calcular_beneficio_bruto(vf, inversion_total)
    
    # Retiro total
    impuesto_total = calcular_impuesto_retiro_total(beneficio_bruto, tipo_bolsa)
    monto_neto_total = calcular_monto_neto_retiro_total(vf, impuesto_total)
    
    # Retiro mensual con impuestos
    tasa_mensual_retiro = calcular_tasa_mensual_retiro(tea)
    retiro_mensual_info = calcular_retiro_mensual_con_impuestos(
        vf, beneficio_bruto, tasa_mensual_retiro, meses_retiro, tipo_bolsa
    )
    
    # Edad de jubilación
    edad_jubilacion = edad_actual + plazo_años
    
    return {
        'plazo_años': plazo_años,
        'edad_jubilacion': edad_jubilacion,
        'tea': tea,
        'vf': vf,
        'inversion_total': inversion_total,
        'beneficio_bruto': beneficio_bruto,
        'impuesto_total': impuesto_total,
        'monto_neto_total': monto_neto_total,
        'retiro_mensual': retiro_mensual_info['retiro_mensual'],
        'capital_neto_mensual': retiro_mensual_info['capital_neto']
    }


def render_comparacion_escenarios(datos_base: dict):
    """
    Renderiza la sección de comparación de escenarios.
    
    Args:
        datos_base: Datos base de la inversión
    """
    st.header("🔄 Comparación de Escenarios")
    
    st.markdown("""
    Compara diferentes escenarios de inversión para tomar mejores decisiones sobre tu jubilación.
    """)
    
    # Seleccionar tipo de comparación
    tipo_comparacion = st.radio(
        "¿Qué deseas comparar?",
        options=["Edades de Jubilación", "Tasas de Retorno", "Ambos"],
        horizontal=True,
        help="Selecciona el tipo de análisis comparativo"
    )
    
    st.divider()
    
    # Variables para comparación
    escenarios = []
    
    if tipo_comparacion == "Edades de Jubilación":
        st.subheader("📅 Comparar Edades de Jubilación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            edad_1 = st.number_input(
                "Edad de jubilación 1",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(60, datos_base["edad_actual"] + 30),
                step=1
            )
        
        with col2:
            edad_2 = st.number_input(
                "Edad de jubilación 2",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(65, datos_base["edad_actual"] + 35),
                step=1
            )
        
        with col3:
            edad_3 = st.number_input(
                "Edad de jubilación 3",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(70, datos_base["edad_actual"] + 40),
                step=1
            )
        
        # Calcular escenarios
        for i, edad in enumerate([edad_1, edad_2, edad_3], 1):
            plazo = edad - datos_base["edad_actual"]
            escenario = calcular_escenario(
                vp=datos_base["valor_presente"],
                aporte=datos_base["aporte_periodico"],
                tea=datos_base["tea"],
                frecuencia_anual=datos_base["frecuencia_anual"],
                plazo_años=plazo,
                tipo_bolsa=datos_base["tipo_bolsa"],
                edad_actual=datos_base["edad_actual"],
                aporte_al_inicio=datos_base["aporte_al_inicio"]
            )
            escenario['nombre'] = f"Jubilación a los {edad} años"
            escenarios.append(escenario)
    
    elif tipo_comparacion == "Tasas de Retorno":
        st.subheader("📈 Comparar Tasas de Retorno")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tea_1 = st.number_input(
                "TEA 1 (%)",
                min_value=0.0,
                max_value=50.0,
                value=max(5.0, datos_base["tea_pct"] - 3),
                step=0.5,
                format="%.2f"
            )
        
        with col2:
            tea_2 = st.number_input(
                "TEA 2 (%)",
                min_value=0.0,
                max_value=50.0,
                value=datos_base["tea_pct"],
                step=0.5,
                format="%.2f"
            )
        
        with col3:
            tea_3 = st.number_input(
                "TEA 3 (%)",
                min_value=0.0,
                max_value=50.0,
                value=min(datos_base["tea_pct"] + 3, 50.0),
                step=0.5,
                format="%.2f"
            )
        
        # Calcular escenarios
        for i, tea_pct in enumerate([tea_1, tea_2, tea_3], 1):
            escenario = calcular_escenario(
                vp=datos_base["valor_presente"],
                aporte=datos_base["aporte_periodico"],
                tea=tea_pct / 100,
                frecuencia_anual=datos_base["frecuencia_anual"],
                plazo_años=datos_base["plazo_años"],
                tipo_bolsa=datos_base["tipo_bolsa"],
                edad_actual=datos_base["edad_actual"],
                aporte_al_inicio=datos_base["aporte_al_inicio"]
            )
            escenario['nombre'] = f"TEA {tea_pct}%"
            escenarios.append(escenario)
    
    else:  # Ambos
        st.subheader("🔀 Comparar Múltiples Factores")
        
        st.markdown("**Escenario Conservador**")
        col1, col2 = st.columns(2)
        with col1:
            edad_cons = st.number_input(
                "Edad de jubilación",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(70, datos_base["edad_actual"] + 40),
                step=1,
                key="edad_cons"
            )
        with col2:
            tea_cons = st.number_input(
                "TEA (%)",
                min_value=0.0,
                max_value=50.0,
                value=max(5.0, datos_base["tea_pct"] - 2),
                step=0.5,
                format="%.2f",
                key="tea_cons"
            )
        
        st.markdown("**Escenario Moderado**")
        col1, col2 = st.columns(2)
        with col1:
            edad_mod = st.number_input(
                "Edad de jubilación",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(65, datos_base["edad_actual"] + 35),
                step=1,
                key="edad_mod"
            )
        with col2:
            tea_mod = st.number_input(
                "TEA (%)",
                min_value=0.0,
                max_value=50.0,
                value=datos_base["tea_pct"],
                step=0.5,
                format="%.2f",
                key="tea_mod"
            )
        
        st.markdown("**Escenario Agresivo**")
        col1, col2 = st.columns(2)
        with col1:
            edad_agr = st.number_input(
                "Edad de jubilación",
                min_value=datos_base["edad_actual"] + 1,
                max_value=100,
                value=min(60, datos_base["edad_actual"] + 30),
                step=1,
                key="edad_agr"
            )
        with col2:
            tea_agr = st.number_input(
                "TEA (%)",
                min_value=0.0,
                max_value=50.0,
                value=min(datos_base["tea_pct"] + 3, 50.0),
                step=0.5,
                format="%.2f",
                key="tea_agr"
            )
        
        # Calcular escenarios
        configs = [
            ("Conservador", edad_cons, tea_cons),
            ("Moderado", edad_mod, tea_mod),
            ("Agresivo", edad_agr, tea_agr)
        ]
        
        for nombre, edad, tea_pct in configs:
            plazo = edad - datos_base["edad_actual"]
            escenario = calcular_escenario(
                vp=datos_base["valor_presente"],
                aporte=datos_base["aporte_periodico"],
                tea=tea_pct / 100,
                frecuencia_anual=datos_base["frecuencia_anual"],
                plazo_años=plazo,
                tipo_bolsa=datos_base["tipo_bolsa"],
                edad_actual=datos_base["edad_actual"],
                aporte_al_inicio=datos_base["aporte_al_inicio"]
            )
            escenario['nombre'] = nombre
            escenarios.append(escenario)
    
    st.divider()
    
    # Mostrar comparación
    if st.button("📊 Generar Comparación", type="primary", use_container_width=True):
        
        st.subheader("📋 Tabla Comparativa")
        
        # Crear DataFrame comparativo
        df_comparacion = pd.DataFrame([
            {
                'Escenario': e['nombre'],
                'Plazo (años)': e['plazo_años'],
                'Edad Jubilación': e['edad_jubilacion'],
                'TEA (%)': f"{e['tea']*100:.2f}%",
                f'Valor Futuro ({MONEDA})': f"{e['vf']:,.2f}",
                f'Inversión Total ({MONEDA})': f"{e['inversion_total']:,.2f}",
                f'Ganancia ({MONEDA})': f"{e['beneficio_bruto']:,.2f}",
                f'Impuesto ({MONEDA})': f"{e['impuesto_total']:,.2f}",
                f'Retiro Mensual ({MONEDA})': f"{e['retiro_mensual']:,.2f}"
            }
            for e in escenarios
        ])
        
        st.dataframe(df_comparacion, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Gráficos comparativos
        st.subheader("📊 Gráficos Comparativos")
        
        tab1, tab2, tab3 = st.tabs(["💰 Valor Futuro", "💳 Retiro Mensual", "📈 Composición"])
        
        with tab1:
            # Gráfico de barras de Valor Futuro
            fig_vf = go.Figure()
            
            fig_vf.add_trace(go.Bar(
                x=[e['nombre'] for e in escenarios],
                y=[e['vf'] for e in escenarios],
                text=[f"{MONEDA} {e['vf']:,.0f}" for e in escenarios],
                textposition='outside',
                marker_color='#4ECDC4',
                hovertemplate='<b>%{x}</b><br>' + f'Valor Futuro: {MONEDA} %{{y:,.2f}}<extra></extra>'
            ))
            
            fig_vf.update_layout(
                title='Comparación de Valor Futuro',
                xaxis_title='Escenario',
                yaxis_title=f'Valor Futuro ({MONEDA})',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig_vf, use_container_width=True)
        
        with tab2:
            # Gráfico de barras de Retiro Mensual
            fig_retiro = go.Figure()
            
            fig_retiro.add_trace(go.Bar(
                x=[e['nombre'] for e in escenarios],
                y=[e['retiro_mensual'] for e in escenarios],
                text=[f"{MONEDA} {e['retiro_mensual']:,.0f}" for e in escenarios],
                textposition='outside',
                marker_color='#FF6B6B',
                hovertemplate='<b>%{x}</b><br>' + f'Retiro Mensual: {MONEDA} %{{y:,.2f}}<extra></extra>'
            ))
            
            fig_retiro.update_layout(
                title='Comparación de Retiro Mensual (20 años)',
                xaxis_title='Escenario',
                yaxis_title=f'Retiro Mensual ({MONEDA})',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig_retiro, use_container_width=True)
        
        with tab3:
            # Gráfico de barras apiladas
            fig_comp = go.Figure()
            
            fig_comp.add_trace(go.Bar(
                name='Inversión',
                x=[e['nombre'] for e in escenarios],
                y=[e['inversion_total'] for e in escenarios],
                marker_color='#95E1D3',
                hovertemplate=f'Inversión: {MONEDA} %{{y:,.2f}}<extra></extra>'
            ))
            
            fig_comp.add_trace(go.Bar(
                name='Ganancia Neta',
                x=[e['nombre'] for e in escenarios],
                y=[e['beneficio_bruto'] - e['impuesto_total'] for e in escenarios],
                marker_color='#4ECDC4',
                hovertemplate=f'Ganancia Neta: {MONEDA} %{{y:,.2f}}<extra></extra>'
            ))
            
            fig_comp.add_trace(go.Bar(
                name='Impuestos',
                x=[e['nombre'] for e in escenarios],
                y=[e['impuesto_total'] for e in escenarios],
                marker_color='#FF6B6B',
                hovertemplate=f'Impuestos: {MONEDA} %{{y:,.2f}}<extra></extra>'
            ))
            
            fig_comp.update_layout(
                title='Composición del Valor Final',
                xaxis_title='Escenario',
                yaxis_title=f'Monto ({MONEDA})',
                barmode='stack',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
        
        st.divider()
        
        # Resumen de recomendación
        st.subheader("💡 Análisis Comparativo")
        
        mejor_vf = max(escenarios, key=lambda x: x['vf'])
        mejor_retiro = max(escenarios, key=lambda x: x['retiro_mensual'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **🏆 Mejor Valor Futuro**
            
            {mejor_vf['nombre']}
            - VF: {MONEDA} {mejor_vf['vf']:,.2f}
            - Plazo: {mejor_vf['plazo_años']} años
            - TEA: {mejor_vf['tea']*100:.2f}%
            """)
        
        with col2:
            st.success(f"""
            **💳 Mejor Retiro Mensual**
            
            {mejor_retiro['nombre']}
            - Retiro: {MONEDA} {mejor_retiro['retiro_mensual']:,.2f}/mes
            - Plazo: {mejor_retiro['plazo_años']} años
            - TEA: {mejor_retiro['tea']*100:.2f}%
            """)
        
        # Descargar comparación
        csv = df_comparacion.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar comparación (CSV)",
            data=csv,
            file_name="comparacion_escenarios.csv",
            mime="text/csv"
        )
