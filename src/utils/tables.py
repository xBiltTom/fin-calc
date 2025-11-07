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


def generar_cronograma_retiros(
    vf: float,
    tasa_mensual_retiro: float,
    meses: int,
    moneda: str = "USD"
) -> pd.DataFrame:
    """
    Genera un cronograma detallado de retiros mensuales.
    
    Args:
        vf: Valor Futuro (saldo inicial para retiros)
        tasa_mensual_retiro: Tasa mensual de retiro (50% de TEA)
        meses: Número de meses de retiro
        moneda: Símbolo de la moneda
    
    Returns:
        DataFrame con columnas: Mes, Saldo Inicial, Interés Generado, 
                                Impuesto (5%), Retiro Bruto, Retiro Neto, Saldo Final
    """
    IMPUESTO_RETIRO_MENSUAL = 0.05
    
    # Calcular retiro mensual bruto
    if tasa_mensual_retiro == 0:
        retiro_mensual_bruto = vf / meses if meses > 0 else 0
    else:
        retiro_mensual_bruto = vf * (tasa_mensual_retiro / (1 - (1 + tasa_mensual_retiro) ** -meses))
    
    data = []
    saldo = vf
    
    for mes in range(1, meses + 1):
        saldo_inicial = saldo
        
        # Interés generado este mes
        interes_mes = saldo_inicial * tasa_mensual_retiro
        
        # Impuesto del 5% sobre el interés
        impuesto_mes = interes_mes * IMPUESTO_RETIRO_MENSUAL
        
        # Retiro neto (retiro bruto - impuesto)
        retiro_neto = retiro_mensual_bruto - impuesto_mes
        
        # Nuevo saldo después del retiro
        saldo_final = saldo_inicial + interes_mes - retiro_mensual_bruto
        
        # Ajustar saldo si es el último mes (por redondeos)
        if mes == meses and abs(saldo_final) < 1:
            saldo_final = 0
        
        data.append({
            'Mes': mes,
            f'Saldo Inicial ({moneda})': round(saldo_inicial, 2),
            f'Interés Generado ({moneda})': round(interes_mes, 2),
            f'Impuesto 5% ({moneda})': round(impuesto_mes, 2),
            f'Retiro Bruto ({moneda})': round(retiro_mensual_bruto, 2),
            f'Retiro Neto ({moneda})': round(retiro_neto, 2),
            f'Saldo Final ({moneda})': round(saldo_final, 2)
        })
        
        saldo = saldo_final
    
    return pd.DataFrame(data)


def generar_resumen_cronograma_retiros(df: pd.DataFrame, moneda: str = "USD") -> dict:
    """
    Genera un resumen estadístico del cronograma de retiros.
    
    Args:
        df: DataFrame con el cronograma de retiros
        moneda: Símbolo de la moneda
    
    Returns:
        Diccionario con estadísticas resumidas
    """
    col_saldo_inicial = f'Saldo Inicial ({moneda})'
    col_interes = f'Interés Generado ({moneda})'
    col_impuesto = f'Impuesto 5% ({moneda})'
    col_retiro_bruto = f'Retiro Bruto ({moneda})'
    col_retiro_neto = f'Retiro Neto ({moneda})'
    
    total_intereses = df[col_interes].sum()
    total_impuestos = df[col_impuesto].sum()
    total_retiro_bruto = df[col_retiro_bruto].sum()
    total_retiro_neto = df[col_retiro_neto].sum()
    saldo_inicial_total = df[col_saldo_inicial].iloc[0]
    
    return {
        'saldo_inicial': saldo_inicial_total,
        'total_intereses': total_intereses,
        'total_impuestos': total_impuestos,
        'total_retiro_bruto': total_retiro_bruto,
        'total_retiro_neto': total_retiro_neto,
        'retiro_mensual_promedio': total_retiro_neto / len(df) if len(df) > 0 else 0
    }
