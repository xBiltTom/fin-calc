def calcular_tasa_periodo(tea: float, frecuencia_anual: int) -> float:
    """
    Convierte la TEA a tasa efectiva del periodo según la frecuencia.
    
    Args:
        tea: Tasa Efectiva Anual (en decimal, ej: 0.10 para 10%)
        frecuencia_anual: Número de periodos por año (12=mensual, 4=trimestral, 2=semestral, 1=anual)
    
    Returns:
        Tasa efectiva del periodo
    """
    return (1 + tea) ** (1 / frecuencia_anual) - 1


def calcular_vf_valor_presente(vp: float, tea: float, periodos: int) -> float:
    """
    Calcula el valor futuro a partir de un valor presente.
    
    Args:
        vp: Valor Presente
        tea: Tasa Efectiva Anual (en decimal)
        periodos: Número de periodos (años)
    
    Returns:
        Valor Futuro
    """
    return vp * (1 + tea) ** periodos


def calcular_vf_aportes_periodicos(aporte: float, tasa_periodo: float, num_periodos: int, aporte_al_inicio: bool = False) -> float:
    """
    Calcula el valor futuro de aportes periódicos.
    
    Args:
        aporte: Monto del aporte periódico
        tasa_periodo: Tasa efectiva del periodo
        num_periodos: Número total de periodos de aporte
        aporte_al_inicio: True si el aporte es al inicio del periodo (anualidad anticipada),
                          False si es al final (anualidad vencida)
    
    Returns:
        Valor Futuro acumulado
    """
    if tasa_periodo == 0:
        return aporte * num_periodos
    
    # Anualidad vencida (aporte al final del periodo)
    vf_vencida = aporte * (((1 + tasa_periodo) ** num_periodos - 1) / tasa_periodo)
    
    # Si es anualidad anticipada (aporte al inicio), multiplicar por (1 + tasa_periodo)
    if aporte_al_inicio:
        return vf_vencida * (1 + tasa_periodo)
    
    return vf_vencida


def calcular_vf_combinado(vp: float, aporte: float, tea: float, frecuencia_anual: int, plazo_años: int, aporte_al_inicio: bool = False) -> float:
    """
    Calcula el valor futuro combinando un valor presente inicial y aportes periódicos.
    
    Args:
        vp: Valor Presente inicial
        aporte: Monto del aporte periódico
        tea: Tasa Efectiva Anual (en decimal)
        frecuencia_anual: Número de periodos por año
        plazo_años: Plazo en años
        aporte_al_inicio: True si el aporte es al inicio del periodo (anualidad anticipada),
                          False si es al final (anualidad vencida)
    
    Returns:
        Valor Futuro total
    """
    tasa_periodo = calcular_tasa_periodo(tea, frecuencia_anual)
    num_periodos = plazo_años * frecuencia_anual
    
    vf_presente = calcular_vf_valor_presente(vp, tea, plazo_años) if vp > 0 else 0
    vf_aportes = calcular_vf_aportes_periodicos(aporte, tasa_periodo, num_periodos, aporte_al_inicio) if aporte > 0 else 0
    
    return vf_presente + vf_aportes


def calcular_beneficio_bruto(vf: float, inversion_total: float) -> float:
    """
    Calcula el beneficio bruto (ganancia antes de impuestos).
    
    Args:
        vf: Valor Futuro
        inversion_total: Inversión total realizada
    
    Returns:
        Beneficio bruto
    """
    return vf - inversion_total
