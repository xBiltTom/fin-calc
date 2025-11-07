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
          - Retiros mensuales programados (con impuestos aplicados)
        - 📈 **Gráficos interactivos** de evolución
        - 📋 **Tabla detallada** de crecimiento periodo a periodo
        - 🎯 **Planificación** por años o edad de jubilación
        - 🔄 **Comparación de escenarios** (edades, tasas, combinados)
        - 📄 **Exportación a PDF** de resultados completos
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Bonos
        
        Calcula el valor presente de bonos considerando:
        
        - 💰 **Valor presente del bono** según tasas de mercado
        - 📅 **Flujos de caja periódicos** detallados
        - 💹 **Cupones** con diferentes frecuencias de pago:
          - Mensual, Bimestral, Trimestral
          - Cuatrimestral, Semestral, Anual
        - � **Tasas efectivas** por periodo
        - 📉 **Análisis de cotización** (Prima/Descuento/Par)
        - 📊 **Gráficos comparativos** de flujos
        - 📄 **Exportación a PDF** de resultados
        """)
    
    st.divider()
    
    # Cómo usar
    st.markdown("""
    ## 🚀 ¿Cómo usar la aplicación?
    
    ### Para Acciones:
    1. **Ve a la sección "Acciones"** desde el menú lateral
    2. **Ingresa tus datos**: edad, inversión inicial, aportes, TEA, tipo de bolsa
    3. **Visualiza los resultados**: Valor Futuro, rentabilidad, proyecciones
    4. **Explora las opciones de retiro**: Total o mensual (ambos con impuestos)
    5. **Compara escenarios**: Diferentes edades de jubilación o tasas de retorno
    6. **Descarga tu reporte**: Exporta resultados en PDF o CSV
    
    ### Para Bonos:
    1. **Ve a la sección "Bonos"** desde el menú lateral
    2. **Ingresa características del bono**: Valor nominal, tasa cupón, frecuencia de pago
    3. **Define condiciones de valoración**: Plazo y tasa de retorno esperada
    4. **Calcula y visualiza**: Valor presente, flujos de caja, gráficos
    5. **Analiza la cotización**: Prima, descuento o a la par
    6. **Descarga resultados**: Exporta tabla de flujos (CSV) o reporte completo (PDF)
    
    ---
    
    ### 💡 Consejos
    
    - Asegúrate de ingresar datos realistas para obtener proyecciones útiles
    - Considera diferentes escenarios de tasas de interés (usa la comparación de escenarios)
    - Revisa el impacto de los impuestos en tus retornos (se aplican automáticamente)
    - Planifica con tiempo suficiente para alcanzar tus metas financieras
    - Descarga los reportes en PDF para guardar tus análisis
    - La TEA está limitada a un máximo de 50% para mantener proyecciones realistas
    """)
    
    st.divider()
    
    # Footer
    st.info("""
    ℹ️ **Nota importante**: Esta herramienta es solo para fines educativos y de planificación. 
    Los resultados son proyecciones basadas en los datos ingresados y no constituyen asesoría financiera profesional.
    """)
    
    # Estadísticas rápidas
    st.markdown("### 📊 Información Clave")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Impuesto Bolsa Nacional",
            value="5%",
            help="Impuesto aplicable a ganancias en bolsa nacional (acciones)"
        )
    
    with col2:
        st.metric(
            label="Impuesto Bolsa Extranjera",
            value="29.5%",
            help="Impuesto aplicable a ganancias en bolsa extranjera (acciones)"
        )
    
    with col3:
        st.metric(
            label="TEA Máxima",
            value="50%",
            help="Tasa Efectiva Anual máxima permitida para proyecciones realistas"
        )
    
    with col4:
        st.metric(
            label="Moneda",
            value="USD",
            help="Todos los cálculos se realizan en dólares estadounidenses"
        )
    
    st.divider()
    
    # Características adicionales
    st.markdown("### ✨ Características Destacadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **📈 Para Inversionistas en Acciones:**
        - Tabla detallada con saldo inicial, aportes e intereses por periodo
        - Comparación de hasta 3 escenarios simultáneos
        - Impuestos aplicados en retiros totales y mensuales
        - Planificación flexible por años o edad de jubilación
        """)
    
    with col2:
        st.info("""
        **📊 Para Inversionistas en Bonos:**
        - Cálculo automático de valor presente del bono
        - Tabla completa de flujos de caja con valores presentes
        - Identificación de tipo de cotización (Prima/Descuento/Par)
        - Soporte para 6 frecuencias diferentes de pago de cupones
        """)
