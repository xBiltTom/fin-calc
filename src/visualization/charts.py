import plotly.graph_objects as go
import pandas as pd
from src.calculations.financial_calcs import calcular_tasa_periodo


def generar_evolucion_inversion(
    vp: float,
    aporte: float,
    tea: float,
    frecuencia_anual: int,
    plazo_años: int,
    aporte_al_inicio: bool = False
) -> pd.DataFrame:
    """
    Genera un DataFrame con la evolución de la inversión periodo a periodo.
    
    Args:
        vp: Valor Presente inicial
        aporte: Aporte periódico
        tea: Tasa Efectiva Anual (en decimal)
        frecuencia_anual: Número de periodos por año
        plazo_años: Plazo en años
        aporte_al_inicio: True si el aporte es al inicio del periodo,
                          False si es al final del periodo
    
    Returns:
        DataFrame con las columnas: periodo, inversion_acumulada, valor_con_interes
    """
    tasa_periodo = calcular_tasa_periodo(tea, frecuencia_anual)
    num_periodos = plazo_años * frecuencia_anual
    
    data = []
    inversion_sin_interes = vp
    valor_con_interes = vp
    
    for periodo in range(num_periodos + 1):
        data.append({
            'periodo': periodo,
            'inversion_acumulada': inversion_sin_interes,
            'valor_con_interes': valor_con_interes
        })
        
        if periodo < num_periodos:
            inversion_sin_interes += aporte
            if aporte_al_inicio:
                # Aporte al inicio: primero se aporta, luego se calcula interés
                valor_con_interes = (valor_con_interes + aporte) * (1 + tasa_periodo)
            else:
                # Aporte al final: primero se calcula interés, luego se aporta
                valor_con_interes = valor_con_interes * (1 + tasa_periodo) + aporte
    
    return pd.DataFrame(data)


def crear_grafico_comparativo(df: pd.DataFrame, moneda: str = "USD") -> go.Figure:
    """
    Crea un gráfico comparativo de la evolución de la inversión.
    
    Args:
        df: DataFrame con la evolución de la inversión
        moneda: Símbolo de la moneda
    
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['inversion_acumulada'],
        mode='lines',
        name='Inversión sin interés',
        line=dict(color='#FF6B6B', width=2),
        hovertemplate=f'<b>Periodo:</b> %{{x}}<br><b>Inversión:</b> {moneda} %{{y:,.2f}}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['valor_con_interes'],
        mode='lines',
        name='Valor con interés',
        line=dict(color='#4ECDC4', width=2),
        fill='tonexty',
        hovertemplate=f'<b>Periodo:</b> %{{x}}<br><b>Valor:</b> {moneda} %{{y:,.2f}}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Evolución de la Inversión',
        xaxis_title='Periodo',
        yaxis_title=f'Monto ({moneda})',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig


def crear_grafico_composicion(
    vp: float,
    total_aportes: float,
    beneficio_bruto: float,
    impuesto: float,
    moneda: str = "USD"
) -> go.Figure:
    """
    Crea un gráfico de torta mostrando la composición del valor final.
    
    Args:
        vp: Valor Presente inicial
        total_aportes: Total de aportes realizados
        beneficio_bruto: Ganancia bruta
        impuesto: Impuesto a pagar
        moneda: Símbolo de la moneda
    
    Returns:
        Figura de Plotly
    """
    labels = []
    values = []
    colors = []
    
    if vp > 0:
        labels.append('Inversión Inicial')
        values.append(vp)
        colors.append('#1f77b4')
    
    if total_aportes > 0:
        labels.append('Aportes Periódicos')
        values.append(total_aportes)
        colors.append('#ff7f0e')
    
    beneficio_neto = beneficio_bruto - impuesto
    if beneficio_neto > 0:
        labels.append('Ganancia Neta')
        values.append(beneficio_neto)
        colors.append('#2ca02c')
    
    if impuesto > 0:
        labels.append('Impuestos')
        values.append(impuesto)
        colors.append('#d62728')
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>' + f'{moneda} %{{value:,.2f}}<br>%{{percent}}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Composición del Valor Final',
        height=400
    )
    
    return fig
