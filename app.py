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
    
    Herramienta para calcular y proyectar inversiones en acciones y bonos.
    
    📅 Versión 1.0
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Secciones disponibles")
    st.sidebar.markdown("""
    - **🏠 Inicio**: Información general
    - **📈 Acciones**: Calculadora activa
    - **📊 Bonos**: Próximamente
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
