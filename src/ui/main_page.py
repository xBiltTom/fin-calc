import streamlit as st
from src.ui.input_form import render_formulario_entrada
from src.ui.display import (
    mostrar_resumen_inversion,
    mostrar_resultados_vf,
    mostrar_resultados_retiro_total,
    mostrar_resultados_retiro_mensual
)
from src.ui.comparacion import render_comparacion_escenarios
from src.calculations.financial_calcs import calcular_vf_combinado, calcular_beneficio_bruto
from src.calculations.tax_calcs import (
    calcular_impuesto_retiro_total,
    calcular_monto_neto_retiro_total,
    calcular_tasa_mensual_retiro,
    calcular_retiro_mensual_con_impuestos
)
from src.visualization.charts import (
    generar_evolucion_inversion,
    crear_grafico_comparativo,
    crear_grafico_composicion
)
from config.constants import MONEDA


def render_acciones_page():
    """
    Renderiza la página de calculadora de acciones.
    """
    st.title("� Calculadora de Acciones")
    st.markdown("""
    Esta herramienta te permite calcular el valor futuro de tus inversiones considerando:
    - 💵 Inversión inicial y/o aportes periódicos
    - 📈 Tasa Efectiva Anual (TEA)
    - 🏛️ Impuestos según tipo de inversión (Nacional 5% / Extranjera 29.5%)
    - 📊 Diferentes formas de retiro (total o mensual)
    """)
    
    st.divider()
    
    # Formulario de entrada
    datos = render_formulario_entrada()
    
    # Validación de datos
    if datos["valor_presente"] <= 0 and datos["aporte_periodico"] <= 0:
        st.warning("⚠️ Debes ingresar al menos una inversión inicial o un aporte periódico.")
        return
    
    st.divider()
    
    # Mostrar resumen
    mostrar_resumen_inversion(datos)
    
    st.divider()
    
    # Calcular Valor Futuro
    vf = calcular_vf_combinado(
        vp=datos["valor_presente"],
        aporte=datos["aporte_periodico"],
        tea=datos["tea"],
        frecuencia_anual=datos["frecuencia_anual"],
        plazo_años=datos["plazo_años"]
    )
    
    # Calcular inversión total y beneficio
    total_aportes = datos["aporte_periodico"] * datos["frecuencia_anual"] * datos["plazo_años"]
    inversion_total = datos["valor_presente"] + total_aportes
    beneficio_bruto = calcular_beneficio_bruto(vf, inversion_total)
    
    # Mostrar resultados VF
    mostrar_resultados_vf(vf, inversion_total, beneficio_bruto)
    
    st.divider()
    
    # Generar y mostrar gráfico de evolución
    st.header("📈 Evolución de la Inversión")
    df_evolucion = generar_evolucion_inversion(
        vp=datos["valor_presente"],
        aporte=datos["aporte_periodico"],
        tea=datos["tea"],
        frecuencia_anual=datos["frecuencia_anual"],
        plazo_años=datos["plazo_años"]
    )
    fig_evolucion = crear_grafico_comparativo(df_evolucion, MONEDA)
    st.plotly_chart(fig_evolucion, use_container_width=True)
    
    st.divider()
    
    # Opciones de retiro
    st.header("💳 Opciones de Retiro")
    
    tipo_retiro = st.radio(
        "Selecciona el tipo de retiro:",
        options=["Retiro Total", "Retiros Mensuales"],
        horizontal=True,
        help="Elige cómo deseas retirar tu inversión"
    )
    
    if tipo_retiro == "Retiro Total":
        # Calcular retiro total con impuestos
        impuesto = calcular_impuesto_retiro_total(beneficio_bruto, datos["tipo_bolsa"])
        monto_neto = calcular_monto_neto_retiro_total(vf, impuesto)
        
        mostrar_resultados_retiro_total(
            vf=vf,
            beneficio_bruto=beneficio_bruto,
            impuesto=impuesto,
            monto_neto=monto_neto,
            tipo_bolsa=datos["tipo_bolsa"]
        )
        
        # Gráfico de composición
        st.subheader("📊 Composición del Valor Final")
        fig_composicion = crear_grafico_composicion(
            vp=datos["valor_presente"],
            total_aportes=total_aportes,
            beneficio_bruto=beneficio_bruto,
            impuesto=impuesto,
            moneda=MONEDA
        )
        st.plotly_chart(fig_composicion, use_container_width=True)
    
    else:  # Retiros Mensuales
        col1, col2 = st.columns(2)
        
        with col1:
            meses_retiro = st.number_input(
                "¿Durante cuántos meses deseas retirar?",
                min_value=1,
                max_value=600,
                value=120,
                step=12,
                help="Periodo durante el cual realizarás retiros mensuales"
            )
        
        with col2:
            st.info(f"📅 Equivale a **{meses_retiro/12:.1f} años** de retiros")
        
        # Calcular retiro mensual con impuestos
        tasa_mensual_retiro = calcular_tasa_mensual_retiro(datos["tea"])
        resultado_retiro = calcular_retiro_mensual_con_impuestos(
            vf=vf,
            beneficio_bruto=beneficio_bruto,
            tasa_mensual_retiro=tasa_mensual_retiro,
            meses=meses_retiro,
            tipo_bolsa=datos["tipo_bolsa"]
        )
        
        mostrar_resultados_retiro_mensual(
            retiro_mensual=resultado_retiro['retiro_mensual'],
            meses=meses_retiro,
            total_retirado=resultado_retiro['total_retirado'],
            capital_neto=resultado_retiro['capital_neto'],
            impuesto=resultado_retiro['impuesto'],
            tipo_bolsa=datos["tipo_bolsa"]
        )
        
        st.info(f"""
        💡 **Nota sobre retiros mensuales:**
        - Se calcula una tasa mensual especial: (1/2) × TEA = {tasa_mensual_retiro*100:.2f}%
        - Se aplican impuestos sobre las ganancias antes de calcular los retiros
        - El capital neto ({MONEDA} {resultado_retiro['capital_neto']:,.2f}) se usa para generar rendimientos durante los retiros
        - El total retirado ({MONEDA} {resultado_retiro['total_retirado']:,.2f}) puede ser mayor al capital neto debido a los intereses generados durante el periodo de retiro
        """)
    
    st.divider()
    
    # Información adicional
    with st.expander("ℹ️ Más información"):
        st.markdown("""
        ### Cómo funciona esta calculadora:
        
        **Cálculo del Valor Futuro (VF):**
        - Si hay inversión inicial: VF = VP × (1 + TEA)^t
        - Si hay aportes periódicos: VF = C × [((1 + i)^n - 1) / i]
        - La tasa se capitaliza según el periodo (mensual, trimestral, etc.)
        
        **Impuestos:**
        - Se aplican sobre la ganancia (VF - Inversión Total)
        - Nacional: 5% | Extranjera: 29.5%
        - Se aplican tanto en retiro total como en retiros mensuales
        
        **Retiros Mensuales:**
        - Utiliza una tasa especial: (1/2) × TEA
        - Se aplican impuestos sobre las ganancias antes de calcular los retiros
        - El capital neto (después de impuestos) se usa para generar los retiros mensuales
        - El capital sigue generando intereses durante los retiros
        
        **Capitalización:**
        - La TEA se convierte a tasa efectiva del periodo
        - Fórmula: tasa_periodo = (1 + TEA)^(1/n) - 1
        - Donde n es la frecuencia anual (12=mensual, 4=trimestral, etc.)
        """)
    
    st.divider()
    
    # Comparación de escenarios
    render_comparacion_escenarios(datos)
