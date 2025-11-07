import pandas as pd
from src.calculations.financial_calcs import calcular_tasa_periodo


def generar_tabla_crecimiento(
    vp: float,
    aporte: float,
    tea: float,
    frecuencia_anual: int,
    plazo_años: int,
    moneda: str = "USD",
    aporte_al_inicio: bool = False
) -> pd.DataFrame:
    """
    Genera una tabla detallada del crecimiento de la inversión periodo a periodo.
    
    Args:
        vp: Valor Presente inicial
        aporte: Aporte periódico
        tea: Tasa Efectiva Anual (en decimal)
        frecuencia_anual: Número de periodos por año
        plazo_años: Plazo en años
        moneda: Símbolo de la moneda
        aporte_al_inicio: True si el aporte es al inicio del periodo,
                          False si es al final del periodo
    
    Returns:
        DataFrame con columnas: Periodo, Saldo Inicial, Aporte, Interés, Saldo Final
    """
    tasa_periodo = calcular_tasa_periodo(tea, frecuencia_anual)
    num_periodos = plazo_años * frecuencia_anual
    
    data = []
    saldo = vp
    
    for periodo in range(1, num_periodos + 1):
        saldo_inicial = saldo
        aporte_periodo = aporte
        
        if aporte_al_inicio:
            # Aporte al inicio: primero se aporta, luego se calcula interés
            base_interes = saldo_inicial + aporte_periodo
            interes_ganado = base_interes * tasa_periodo
            saldo_final = base_interes + interes_ganado
        else:
            # Aporte al final: primero se calcula interés, luego se aporta
            interes_ganado = saldo_inicial * tasa_periodo
            saldo_final = saldo_inicial + interes_ganado + aporte_periodo
        
        data.append({
            'Periodo': periodo,
            f'Saldo Inicial ({moneda})': round(saldo_inicial, 2),
            f'Aporte ({moneda})': round(aporte_periodo, 2),
            f'Interés Ganado ({moneda})': round(interes_ganado, 2),
            f'Saldo Final ({moneda})': round(saldo_final, 2)
        })
        
        saldo = saldo_final
    
    return pd.DataFrame(data)


def formatear_tabla_crecimiento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formatea la tabla de crecimiento para visualización.
    
    Args:
        df: DataFrame con los datos de crecimiento
    
    Returns:
        DataFrame formateado para mostrar
    """
    df_formatted = df.copy()
    
    # Formatear columnas numéricas
    for col in df_formatted.columns:
        if col != 'Periodo':
            df_formatted[col] = df_formatted[col].apply(lambda x: f"{x:,.2f}")
    
    return df_formatted


def generar_resumen_tabla(df: pd.DataFrame, moneda: str = "USD") -> dict:
    """
    Genera un resumen estadístico de la tabla de crecimiento.
    
    Args:
        df: DataFrame con los datos de crecimiento
        moneda: Símbolo de la moneda
    
    Returns:
        Diccionario con estadísticas resumidas
    """
    col_saldo_inicial = f'Saldo Inicial ({moneda})'
    col_aporte = f'Aporte ({moneda})'
    col_interes = f'Interés Ganado ({moneda})'
    col_saldo_final = f'Saldo Final ({moneda})'
    
    total_aportes = df[col_aporte].sum()
    total_intereses = df[col_interes].sum()
    saldo_inicial_total = df[col_saldo_inicial].iloc[0]
    saldo_final_total = df[col_saldo_final].iloc[-1]
    
    return {
        'saldo_inicial': saldo_inicial_total,
        'total_aportes': total_aportes,
        'total_intereses': total_intereses,
        'saldo_final': saldo_final_total,
        'ganancia_total': saldo_final_total - saldo_inicial_total - total_aportes
    }
