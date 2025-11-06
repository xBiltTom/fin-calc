import streamlit as st
from config.constants import FRECUENCIAS_BONOS, MONEDA
from src.calculations.bond_calcs import calcular_valor_presente_bono
from src.visualization.bond_charts import (
    crear_grafico_flujos_bono,
    crear_grafico_valor_presente,
    crear_tabla_flujos,
    crear_grafico_composicion_bono
)
from src.utils.pdf_generator import crear_pdf_bonos


def render_bonos_page():
    """
    Renderiza la página de calculadora de bonos.
    """
    st.title("📊 Calculadora de Bonos")
    st.markdown("""
    Calcula el valor presente de un bono considerando sus flujos de caja periódicos, 
    tasa cupón y tasa de retorno esperada.
    """)
    
    st.divider()
    
    # Formulario de entrada
    st.header("📋 Datos del Bono")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Características del Bono")
        
        valor_nominal = st.number_input(
            f"Valor Nominal ({MONEDA})",
            min_value=100.0,
            value=1000.0,
            step=100.0,
            format="%.2f",
            help="Valor facial del bono que se pagará al vencimiento"
        )
        
        tasa_cupon_pct = st.number_input(
            "Tasa Cupón (% TEA)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5,
            format="%.2f",
            help="Tasa de interés anual que paga el bono"
        )
        
        frecuencia_pago = st.selectbox(
            "Frecuencia de Pago",
            options=list(FRECUENCIAS_BONOS.keys()),
            index=5,  # Anual por defecto
            help="¿Con qué frecuencia se pagan los cupones?"
        )
    
    with col2:
        st.subheader("Condiciones de Valoración")
        
        plazo_años = st.number_input(
            "Plazo (años)",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
            help="Años hasta el vencimiento del bono"
        )
        
        tea_descuento_pct = st.number_input(
            "Tasa de Retorno Esperada (% TEA)",
            min_value=0.0,
            max_value=100.0,
            value=6.0,
            step=0.5,
            format="%.2f",
            help="Tasa de descuento para calcular el valor presente"
        )
        
        st.info(f"💡 Frecuencia seleccionada: **{FRECUENCIAS_BONOS[frecuencia_pago]} pagos/año**")
    
    st.divider()
    
    # Botón de cálculo
    if st.button("🧮 Calcular Valor Presente del Bono", type="primary", use_container_width=True):
        
        # Convertir porcentajes a decimales
        tasa_cupon_anual = tasa_cupon_pct / 100
        tea_descuento = tea_descuento_pct / 100
        frecuencia_anual = FRECUENCIAS_BONOS[frecuencia_pago]
        
        # Calcular valor presente del bono
        resultado = calcular_valor_presente_bono(
            valor_nominal=valor_nominal,
            tasa_cupon_anual=tasa_cupon_anual,
            frecuencia_anual=frecuencia_anual,
            años=plazo_años,
            tea_descuento=tea_descuento
        )
        
        st.divider()
        
        # Mostrar resultados principales
        st.header("💰 Resultados de la Valoración")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Valor Presente del Bono",
                value=f"{MONEDA} {resultado['valor_presente_total']:,.2f}",
                delta=f"{((resultado['valor_presente_total'] / valor_nominal - 1) * 100):.2f}%",
                delta_color="off",
                help="Precio teórico del bono hoy"
            )
        
        with col2:
            st.metric(
                label="Cupón Periódico",
                value=f"{MONEDA} {resultado['cupon_periodico']:,.2f}",
                help="Monto de cada pago de cupón"
            )
        
        with col3:
            st.metric(
                label="Número de Pagos",
                value=f"{resultado['num_periodos']}",
                help="Total de cupones a recibir"
            )
        
        with col4:
            total_cupones = resultado['cupon_periodico'] * resultado['num_periodos']
            st.metric(
                label="Total en Cupones",
                value=f"{MONEDA} {total_cupones:,.2f}",
                help="Suma de todos los cupones"
            )
        
        st.divider()
        
        # Información adicional
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Tasas Efectivas por Periodo")
            st.markdown(f"""
            - **Tasa Cupón por periodo**: {resultado['tasa_cupon_periodo']*100:.4f}%
            - **Tasa Descuento por periodo**: {resultado['tasa_descuento_periodo']*100:.4f}%
            - **Frecuencia**: {frecuencia_pago} ({frecuencia_anual} veces/año)
            """)
        
        with col2:
            st.subheader("💡 Interpretación")
            if resultado['valor_presente_total'] > valor_nominal:
                st.success(f"""
                **Bono con Prima** 🟢
                
                El bono cotiza por encima de su valor nominal 
                ({((resultado['valor_presente_total'] / valor_nominal - 1) * 100):.2f}% más).
                Esto ocurre cuando la tasa cupón es mayor que la tasa de retorno esperada.
                """)
            elif resultado['valor_presente_total'] < valor_nominal:
                st.warning(f"""
                **Bono con Descuento** 🟡
                
                El bono cotiza por debajo de su valor nominal 
                ({((1 - resultado['valor_presente_total'] / valor_nominal) * 100):.2f}% menos).
                Esto ocurre cuando la tasa cupón es menor que la tasa de retorno esperada.
                """)
            else:
                st.info("""
                **Bono a la Par** 🔵
                
                El bono cotiza a su valor nominal.
                La tasa cupón es igual a la tasa de retorno esperada.
                """)
        
        st.divider()
        
        # Gráficos
        st.header("📈 Visualización de Flujos")
        
        tab1, tab2, tab3 = st.tabs(["📊 Flujos de Caja", "💵 Comparativa VP", "🥧 Composición"])
        
        with tab1:
            st.subheader("Flujos de Caja Periódicos")
            fig_flujos = crear_grafico_flujos_bono(resultado['flujos'], MONEDA)
            st.plotly_chart(fig_flujos, use_container_width=True)
            
            st.info("""
            💡 **Nota**: El último flujo (en rojo) incluye el cupón final más el valor nominal del bono.
            """)
        
        with tab2:
            st.subheader("Flujos Nominales vs Valores Presentes")
            fig_vp = crear_grafico_valor_presente(resultado['flujos'], MONEDA)
            st.plotly_chart(fig_vp, use_container_width=True)
            
            st.info("""
            💡 **Nota**: Los valores presentes son menores debido al descuento temporal del dinero.
            """)
        
        with tab3:
            # Calcular VP de cupones sin el principal
            vp_cupones = sum([f['vp_flujo'] for f in resultado['flujos'][:-1]])
            vp_ultimo = resultado['flujos'][-1]['vp_flujo']
            vp_principal_estimado = vp_ultimo - (resultado['cupon_periodico'] / ((1 + resultado['tasa_descuento_periodo']) ** resultado['num_periodos']))
            
            st.subheader("Composición del Valor Presente")
            fig_comp = crear_grafico_composicion_bono(
                vp_cupones + (resultado['cupon_periodico'] / ((1 + resultado['tasa_descuento_periodo']) ** resultado['num_periodos'])),
                vp_principal_estimado,
                MONEDA
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        
        st.divider()
        
        # Tabla detallada de flujos
        st.header("📋 Tabla Detallada de Flujos")
        
        df_flujos = crear_tabla_flujos(resultado['flujos'], MONEDA)
        
        # Mostrar tabla con opciones de paginación
        st.dataframe(
            df_flujos,
            use_container_width=True,
            hide_index=True,
            height=min(400, 35 * len(df_flujos) + 38)
        )
        
        # Totales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_flujos = sum([f['flujo'] for f in resultado['flujos']])
            st.metric(
                label="Total Flujos Nominales",
                value=f"{MONEDA} {total_flujos:,.2f}"
            )
        
        with col2:
            st.metric(
                label="Total Valor Presente",
                value=f"{MONEDA} {resultado['valor_presente_total']:,.2f}"
            )
        
        with col3:
            diferencia = total_flujos - resultado['valor_presente_total']
            st.metric(
                label="Descuento Temporal",
                value=f"{MONEDA} {diferencia:,.2f}",
                delta=f"-{(diferencia/total_flujos*100):.2f}%",
                delta_color="inverse"
            )
        
        st.divider()
        
        # Botones de descarga
        st.header("📄 Exportar Resultados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Descargar CSV
            csv = df_flujos.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar tabla de flujos (CSV)",
                data=csv,
                file_name=f"flujos_bono_{valor_nominal}_{tasa_cupon_pct}pct.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Preparar datos para el PDF
            datos_entrada_pdf = {
                'valor_nominal': valor_nominal,
                'tasa_cupon_pct': tasa_cupon_pct,
                'frecuencia': frecuencia_pago,
                'plazo_años': plazo_años,
                'tea_descuento_pct': tea_descuento_pct
            }
            
            # Generar PDF
            pdf_buffer = crear_pdf_bonos(
                datos_entrada=datos_entrada_pdf,
                resultados=resultado,
                df_flujos=df_flujos
            )
            
            st.download_button(
                label="📥 Descargar Reporte PDF",
                data=pdf_buffer,
                file_name=f"reporte_bono_{valor_nominal}_{tasa_cupon_pct}pct.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
    
    else:
        st.info("👆 Ingresa los datos del bono y presiona el botón para calcular su valor presente.")
    
    st.divider()
    
    # Información adicional
    with st.expander("ℹ️ ¿Cómo se calcula el valor presente de un bono?"):
        st.markdown("""
        ### Fórmula del Valor Presente de un Bono
        
        El valor presente (VP) de un bono se calcula como la suma de:
        
        1. **Valor presente de todos los cupones**:
        $$VP_{cupones} = \\sum_{t=1}^{n} \\frac{C}{(1 + i)^t}$$
        
        2. **Valor presente del valor nominal**:
        $$VP_{nominal} = \\frac{VN}{(1 + i)^n}$$
        
        Donde:
        - **C**: Cupón periódico = VN × tasa_cupón_periodo
        - **VN**: Valor Nominal del bono
        - **i**: Tasa de descuento por periodo
        - **n**: Número total de periodos
        - **t**: Periodo actual (1, 2, 3, ..., n)
        
        ### Conversión de Tasas
        
        Las tasas efectivas anuales (TEA) se convierten a tasas por periodo usando:
        
        $$tasa_{periodo} = (1 + TEA)^{1/f} - 1$$
        
        Donde **f** es la frecuencia de pagos por año.
        
        ### Tipos de Cotización
        
        - **Prima**: VP > Valor Nominal (tasa cupón > tasa de mercado)
        - **Descuento**: VP < Valor Nominal (tasa cupón < tasa de mercado)
        - **A la Par**: VP = Valor Nominal (tasa cupón = tasa de mercado)
        """)

