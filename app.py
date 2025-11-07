import streamlit as st
from src.ui.inicio_page import render_inicio_page
from src.ui.main_page import render_acciones_page
from src.ui.bonos_page import render_bonos_page

st.set_page_config(
    page_title="Calculadora Financiera",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Sidebar para navegación
    st.sidebar.title("🧭 Navegación")
    st.sidebar.markdown("---")
    
    # Opciones de navegación
    pagina = st.sidebar.radio(
        "Selecciona una sección:",
        ["🏠 Inicio", "📈 Acciones", "📊 Bonos"],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Información adicional en sidebar
    st.sidebar.markdown("### 💡 Acerca de")
    st.sidebar.info("""
    **Calculadora Financiera**
    
    Herramienta completa para calcular y proyectar inversiones en acciones y bonos.
    
    ✅ Todas las funcionalidades activas
    📅 Versión 1.0
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Secciones")
    st.sidebar.success("""
    **🏠 Inicio**
    Información general y guía de uso
    
    **📈 Acciones**
    - Valor futuro de inversiones
    - Retiros con impuestos
    - Comparación de escenarios
    - Tabla detallada de crecimiento
    - Exportación a PDF
    
    **📊 Bonos**
    - Valoración de bonos
    - Flujos de caja periódicos
    - Análisis de cotización
    - Exportación a PDF
    """)
    
    # Renderizar la página seleccionada
    if pagina == "🏠 Inicio":
        render_inicio_page()
    elif pagina == "📈 Acciones":
        render_acciones_page()
    elif pagina == "📊 Bonos":
        render_bonos_page()

if __name__ == "__main__":
    main()
