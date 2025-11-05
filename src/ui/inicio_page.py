import streamlit as st


def render_inicio_page():
    """
    Renderiza la página de inicio con información sobre la aplicación.
    """
    st.title("💰 Calculadora Financiera")
    st.markdown("### Bienvenido a tu herramienta de planificación financiera")
    
    st.divider()
    
    # Introducción
    st.markdown("""
    ## 📋 ¿Qué es esta aplicación?
    
    Esta es una herramienta completa para calcular y proyectar tus inversiones en **acciones** y **bonos**, 
    considerando todos los factores importantes como tasas de interés, impuestos y diferentes estrategias de retiro.
    """)
    
    st.divider()
    
    # Características principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Acciones
        
        Calcula el valor futuro de tus inversiones en acciones con:
        
        - 💵 **Inversión inicial** y/o **aportes periódicos**
        - 📊 **Capitalización** según frecuencia (mensual, trimestral, semestral, anual)
        - 🏛️ **Impuestos diferenciados**:
          - Nacional: 5%
          - Extranjera: 29.5%
        - 💳 **Modalidades de retiro**:
          - Retiro total con impuestos
          - Retiros mensuales programados
        - 📈 **Gráficos interactivos** de evolución
        - 🎯 **Planificación** por años o edad de jubilación
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Bonos
        
        *Próximamente disponible*
        
        Podrás calcular:
        
        - 💰 Valor presente y futuro de bonos
        - 📅 Flujos de caja periódicos
        - 💹 Rendimiento al vencimiento (YTM)
        - 🔄 Valor de cupones
        - 📉 Duration y convexidad
        - 🏦 Bonos con diferentes frecuencias de pago
        
        *Esta funcionalidad estará disponible próximamente*
        """)
    
    st.divider()
    
    # Cómo usar
    st.markdown("""
    ## 🚀 ¿Cómo usar la aplicación?
    
    1. **Selecciona una sección** desde el menú lateral (sidebar)
    2. **Ingresa tus datos** de inversión
    3. **Visualiza los resultados** y proyecciones
    4. **Analiza los gráficos** para tomar mejores decisiones
    
    ---
    
    ### 💡 Consejos
    
    - Asegúrate de ingresar datos realistas para obtener proyecciones útiles
    - Considera diferentes escenarios de tasas de interés
    - Revisa el impacto de los impuestos en tus retornos
    - Planifica con tiempo suficiente para alcanzar tus metas financieras
    """)
    
    st.divider()
    
    # Footer
    st.info("""
    ℹ️ **Nota importante**: Esta herramienta es solo para fines educativos y de planificación. 
    Los resultados son proyecciones basadas en los datos ingresados y no constituyen asesoría financiera profesional.
    """)
    
    # Estadísticas rápidas (decorativo)
    st.markdown("### 📊 Datos de interés")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Impuesto Bolsa Nacional",
            value="5%",
            help="Impuesto aplicable a ganancias en bolsa nacional"
        )
    
    with col2:
        st.metric(
            label="Impuesto Bolsa Extranjera",
            value="29.5%",
            help="Impuesto aplicable a ganancias en bolsa extranjera"
        )
    
    with col3:
        st.metric(
            label="Moneda",
            value="USD",
            help="Todos los cálculos se realizan en dólares"
        )
