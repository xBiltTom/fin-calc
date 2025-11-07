import streamlit as st
import pandas as pd
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
from src.utils.tables import (
    generar_tabla_crecimiento,
    formatear_tabla_crecimiento,
    generar_resumen_tabla
)
from src.utils.pdf_generator import crear_pdf_acciones
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
        plazo_años=datos["plazo_años"],
        aporte_al_inicio=datos["aporte_al_inicio"]
    )
    
    # Calcular inversión total y beneficio
    total_aportes = datos["aporte_periodico"] * datos["frecuencia_anual"] * datos["plazo_años"]
    inversion_total = datos["valor_presente"] + total_aportes
    beneficio_bruto = calcular_beneficio_bruto(vf, inversion_total)
    
    # Generar tabla de crecimiento (se usará para PDF y visualización)
    df_tabla_crecimiento = generar_tabla_crecimiento(
        vp=datos["valor_presente"],
        aporte=datos["aporte_periodico"],
        tea=datos["tea"],
        frecuencia_anual=datos["frecuencia_anual"],
        plazo_años=datos["plazo_años"],
        moneda=MONEDA,
        aporte_al_inicio=datos["aporte_al_inicio"]
    )
    
    # Mostrar resultados VF
    mostrar_resultados_vf(vf, inversion_total, beneficio_bruto)
    
    st.divider()
    
    # Generar y mostrar gráfico de evolución
    st.header("📈 Evolución de la Inversión")
    
    # Tabs para gráfico y tabla
    tab1, tab2 = st.tabs(["📊 Gráfico", "📋 Tabla Detallada"])
    
    with tab1:
        df_evolucion = generar_evolucion_inversion(
            vp=datos["valor_presente"],
            aporte=datos["aporte_periodico"],
            tea=datos["tea"],
            frecuencia_anual=datos["frecuencia_anual"],
            plazo_años=datos["plazo_años"],
            aporte_al_inicio=datos["aporte_al_inicio"]
        )
        fig_evolucion = crear_grafico_comparativo(df_evolucion, MONEDA)
        st.plotly_chart(fig_evolucion, use_container_width=True)
    
    with tab2:
        st.subheader("📋 Tabla de Crecimiento Detallada")
        
        # Usar la tabla ya generada
        df_tabla = df_tabla_crecimiento
        
        # Mostrar resumen de la tabla
        resumen = generar_resumen_tabla(df_tabla, MONEDA)
        
        st.markdown("#### 📊 Resumen General")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Saldo Inicial",
                value=f"{MONEDA} {resumen['saldo_inicial']:,.2f}"
            )
        
        with col2:
            st.metric(
                label="Total Aportes",
                value=f"{MONEDA} {resumen['total_aportes']:,.2f}"
            )
        
        with col3:
            st.metric(
                label="Total Intereses",
                value=f"{MONEDA} {resumen['total_intereses']:,.2f}",
                delta="Ganado"
            )
        
        with col4:
            st.metric(
                label="Saldo Final",
                value=f"{MONEDA} {resumen['saldo_final']:,.2f}",
                delta=f"+{((resumen['saldo_final']/resumen['saldo_inicial'] - 1) * 100):.1f}%" if resumen['saldo_inicial'] > 0 else "N/A"
            )
        
        st.divider()
        
        # Mostrar tabla con paginación
        st.markdown("#### 📋 Detalle por Periodo")
        
        # Opciones de visualización
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info(f"📌 Total de periodos: **{len(df_tabla)}** | Frecuencia: **{datos['frecuencia']}**")
        
        with col2:
            mostrar_todos = st.checkbox("Mostrar todos", value=False)
        
        if not mostrar_todos and len(df_tabla) > 20:
            st.warning(f"⚠️ Mostrando primeros 20 periodos de {len(df_tabla)}. Activa 'Mostrar todos' para ver la tabla completa.")
            df_mostrar = df_tabla.head(20)
        else:
            df_mostrar = df_tabla
        
        # Formatear y mostrar tabla
        df_formatted = formatear_tabla_crecimiento(df_mostrar)
        
        st.dataframe(
            df_formatted,
            use_container_width=True,
            hide_index=True,
            height=min(600, 35 * len(df_mostrar) + 38)
        )
        
        # Información adicional
        if len(df_tabla) > 20 and not mostrar_todos:
            st.info(f"💡 Se están ocultando {len(df_tabla) - 20} periodos. Descarga la tabla completa o activa 'Mostrar todos'.")
        
        # Botón de descarga
        csv = df_tabla.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Descargar tabla completa (CSV) - {len(df_tabla)} periodos",
            data=csv,
            file_name=f"crecimiento_inversion_{datos['plazo_años']}años.csv",
            mime="text/csv",
            use_container_width=True
        )
    
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
            tipo_bolsa=datos["tipo_bolsa"],
            retiro_mensual_bruto=resultado_retiro.get('retiro_mensual_bruto')
        )
        
        st.info(f"""
        💡 **Nota sobre retiros mensuales:**
        - Base de cálculo: Valor Futuro completo ({MONEDA} {vf:,.2f})
        - Tasa mensual de retiro: (1/2) × TEA = {tasa_mensual_retiro*100:.2f}%
        - Impuesto del **5%** aplicado mensualmente solo a los intereses generados
        - Retiro mensual bruto: {MONEDA} {resultado_retiro.get('retiro_mensual_bruto', 0):,.2f}
        - Impuestos totales sobre intereses: {MONEDA} {resultado_retiro['impuesto']:,.2f}
        - Total neto a retirar: {MONEDA} {resultado_retiro['total_retirado']:,.2f}
        """)
        
        st.divider()
        
        # Cronograma de retiros
        st.subheader("📅 Cronograma de Retiros Mensuales")
        
        from src.utils.tables import generar_cronograma_retiros, generar_resumen_cronograma_retiros
        
        # Generar cronograma
        df_cronograma = generar_cronograma_retiros(
            vf=vf,
            tasa_mensual_retiro=tasa_mensual_retiro,
            meses=meses_retiro,
            moneda=MONEDA
        )
        
        # Resumen del cronograma
        resumen_cronograma = generar_resumen_cronograma_retiros(df_cronograma, MONEDA)
        
        st.markdown("#### 📊 Resumen del Cronograma")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Saldo Inicial",
                value=f"{MONEDA} {resumen_cronograma['saldo_inicial']:,.2f}"
            )
        
        with col2:
            st.metric(
                label="Total Intereses",
                value=f"{MONEDA} {resumen_cronograma['total_intereses']:,.2f}",
                delta="Ganado"
            )
        
        with col3:
            st.metric(
                label="Total Impuestos (5%)",
                value=f"{MONEDA} {resumen_cronograma['total_impuestos']:,.2f}",
                delta=f"-{MONEDA} {resumen_cronograma['total_impuestos']:,.2f}",
                delta_color="inverse"
            )
        
        with col4:
            st.metric(
                label="Total Neto Retirado",
                value=f"{MONEDA} {resumen_cronograma['total_retiro_neto']:,.2f}"
            )
        
        st.divider()
        
        # Mostrar tabla con opciones
        st.markdown("#### 📋 Detalle Mes a Mes")
        
        # Opciones de visualización
        col1, col2 = st.columns([2, 1])
        
        with col1:
            mostrar_todos_meses = st.checkbox(
                "Mostrar todos los meses",
                value=False,
                help="Si está desmarcado, muestra solo los primeros 12 y últimos 12 meses"
            )
        
        with col2:
            formato_miles = st.checkbox(
                "Formato con separador de miles",
                value=True,
                help="Mostrar números con comas como separadores"
            )
        
        # Preparar tabla para mostrar
        if mostrar_todos_meses:
            df_mostrar = df_cronograma.copy()
        else:
            if len(df_cronograma) > 24:
                df_primeros = df_cronograma.head(12)
                df_ultimos = df_cronograma.tail(12)
                df_mostrar = pd.concat([df_primeros, df_ultimos])
                st.info(f"📌 Mostrando los primeros 12 y últimos 12 meses de {meses_retiro} meses totales")
            else:
                df_mostrar = df_cronograma.copy()
        
        # Formatear para visualización
        if formato_miles:
            df_display = df_mostrar.copy()
            for col in df_display.columns:
                if col != 'Mes':
                    df_display[col] = df_display[col].apply(lambda x: f"{x:,.2f}")
            st.dataframe(df_display, use_container_width=True, height=400)
        else:
            st.dataframe(df_mostrar, use_container_width=True, height=400)
    
    st.divider()
    
    # Botón para exportar a PDF
    st.header("📄 Exportar Resultados")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("💾 Descarga un reporte completo en PDF con todos los resultados de tu inversión")
    
    with col2:
        # Preparar datos para el PDF
        resultados_vf_pdf = {
            'vf': vf,
            'inversion_total': inversion_total,
            'beneficio_bruto': beneficio_bruto
        }
        
        if tipo_retiro == "Retiro Total":
            resultados_retiro_pdf = {
                'vf': vf,
                'impuesto': impuesto,
                'monto_neto': monto_neto
            }
            tipo_retiro_pdf = "total"
        else:
            resultados_retiro_pdf = {
                'vf': vf,
                'impuesto': resultado_retiro['impuesto'],
                'capital_neto': resultado_retiro['capital_neto'],
                'retiro_mensual': resultado_retiro['retiro_mensual'],
                'meses': meses_retiro,
                'total_retirado': resultado_retiro['total_retirado']
            }
            tipo_retiro_pdf = "mensual"
        
        # Generar PDF
        pdf_buffer = crear_pdf_acciones(
            datos_entrada=datos,
            resultados_vf=resultados_vf_pdf,
            resultados_retiro=resultados_retiro_pdf,
            tipo_retiro=tipo_retiro_pdf,
            df_tabla=df_tabla_crecimiento
        )
        
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_buffer,
            file_name=f"reporte_acciones_{datos['plazo_años']}años.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    
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
