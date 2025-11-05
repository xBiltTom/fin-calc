# Calculadora Financiera

Aplicación de Streamlit para calcular el valor futuro de inversiones con impuestos.

## Estructura del Proyecto

```
fin-calc/
├── app.py                          # Punto de entrada de la aplicación
├── requirements.txt                # Dependencias
├── config/
│   ├── __init__.py
│   └── constants.py               # Constantes globales
├── src/
│   ├── __init__.py
│   ├── calculations/              # Módulos de cálculos
│   │   ├── __init__.py
│   │   ├── financial_calcs.py    # Cálculos financieros (VF, TEA, etc.)
│   │   └── tax_calcs.py          # Cálculos de impuestos
│   ├── visualization/             # Módulos de visualización
│   │   ├── __init__.py
│   │   └── charts.py             # Gráficos con Plotly
│   ├── ui/                        # Componentes de interfaz
│   │   ├── __init__.py
│   │   ├── input_form.py         # Formularios de entrada
│   │   ├── display.py            # Componentes de visualización
│   │   └── main_page.py          # Página principal
│   └── utils/                     # Utilidades
│       ├── __init__.py
│       └── helpers.py            # Funciones auxiliares
└── assets/                        # Recursos estáticos
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

## Características

- 💵 Cálculo con inversión inicial y/o aportes periódicos
- 📈 Capitalización según frecuencia (mensual, trimestral, semestral, anual)
- 🏛️ Impuestos diferenciados (Nacional 5% / Extranjera 29.5%)
- 💳 Dos modalidades de retiro (total o mensual)
- 📊 Gráficos interactivos de evolución
- 🎯 Cálculo por plazo en años o edad de jubilación
