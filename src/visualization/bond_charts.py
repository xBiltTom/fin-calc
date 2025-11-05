import plotly.graph_objects as go
import pandas as pd


def crear_grafico_flujos_bono(flujos: list, moneda: str = "USD") -> go.Figure:
    """
    Crea un gráfico de barras mostrando los flujos de caja del bono.
    
    Args:
        flujos: Lista de diccionarios con información de flujos
        moneda: Símbolo de la moneda
    
    Returns:
        Figura de Plotly
    """
    df = pd.DataFrame(flujos)
    
    # Colores diferentes para el último flujo (incluye principal)
    colors = ['#4ECDC4' if not f['es_ultimo'] else '#FF6B6B' for f in flujos]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['periodo'],
        y=df['flujo'],
        marker_color=colors,
        text=df['flujo'].apply(lambda x: f'{moneda} {x:,.2f}'),
        textposition='outside',
        hovertemplate=f'<b>Periodo:</b> %{{x}}<br><b>Flujo:</b> {moneda} %{{y:,.2f}}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Flujos de Caja del Bono',
        xaxis_title='Periodo',
        yaxis_title=f'Flujo ({moneda})',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig


def crear_grafico_valor_presente(flujos: list, moneda: str = "USD") -> go.Figure:
    """
    Crea un gráfico comparativo entre flujos nominales y valores presentes.
    
    Args:
        flujos: Lista de diccionarios con información de flujos
        moneda: Símbolo de la moneda
    
    Returns:
        Figura de Plotly
    """
    df = pd.DataFrame(flujos)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['periodo'],
        y=df['flujo'],
        name='Flujo Nominal',
        marker_color='#95E1D3',
        hovertemplate=f'<b>Periodo:</b> %{{x}}<br><b>Flujo Nominal:</b> {moneda} %{{y:,.2f}}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=df['periodo'],
        y=df['vp_flujo'],
        name='Valor Presente',
        marker_color='#4ECDC4',
        hovertemplate=f'<b>Periodo:</b> %{{x}}<br><b>Valor Presente:</b> {moneda} %{{y:,.2f}}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Flujos Nominales vs Valores Presentes',
        xaxis_title='Periodo',
        yaxis_title=f'Monto ({moneda})',
        barmode='group',
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


def crear_tabla_flujos(flujos: list, moneda: str = "USD") -> pd.DataFrame:
    """
    Crea un DataFrame con el detalle de flujos para mostrar en tabla.
    
    Args:
        flujos: Lista de diccionarios con información de flujos
        moneda: Símbolo de la moneda
    
    Returns:
        DataFrame con los flujos formateados
    """
    data = []
    for f in flujos:
        data.append({
            'Periodo': f['periodo'],
            f'Flujo ({moneda})': f'{f["flujo"]:,.2f}',
            f'Valor Presente ({moneda})': f'{f["vp_flujo"]:,.2f}',
            'Tipo': 'Cupón + Principal' if f['es_ultimo'] else 'Cupón'
        })
    
    return pd.DataFrame(data)


def crear_grafico_composicion_bono(
    vp_cupones: float,
    vp_principal: float,
    moneda: str = "USD"
) -> go.Figure:
    """
    Crea un gráfico de torta mostrando la composición del valor presente del bono.
    
    Args:
        vp_cupones: Valor presente de los cupones
        vp_principal: Valor presente del principal
        moneda: Símbolo de la moneda
    
    Returns:
        Figura de Plotly
    """
    labels = ['Valor Presente de Cupones', 'Valor Presente del Principal']
    values = [vp_cupones, vp_principal]
    colors = ['#4ECDC4', '#FF6B6B']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>' + f'{moneda} %{{value:,.2f}}<br>%{{percent}}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Composición del Valor Presente del Bono',
        height=400
    )
    
    return fig
