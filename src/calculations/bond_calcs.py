def calcular_tasa_cupon_periodo(tasa_cupon_anual: float, frecuencia_anual: int) -> float:
    """
    Calcula la tasa de cupón por periodo.
    
    Args:
        tasa_cupon_anual: Tasa cupón anual (TEA) en decimal
        frecuencia_anual: Número de pagos por año
    
    Returns:
        Tasa de cupón por periodo
    """
    return (1 + tasa_cupon_anual) ** (1 / frecuencia_anual) - 1


def calcular_tasa_descuento_periodo(tea_descuento: float, frecuencia_anual: int) -> float:
    """
    Calcula la tasa de descuento por periodo.
    
    Args:
        tea_descuento: Tasa efectiva anual de descuento en decimal
        frecuencia_anual: Número de pagos por año
    
    Returns:
        Tasa de descuento por periodo
    """
    return (1 + tea_descuento) ** (1 / frecuencia_anual) - 1


def calcular_cupon(valor_nominal: float, tasa_cupon_periodo: float) -> float:
    """
    Calcula el monto del cupón periódico.
    
    Args:
        valor_nominal: Valor nominal del bono
        tasa_cupon_periodo: Tasa de cupón por periodo
    
    Returns:
        Monto del cupón
    """
    return valor_nominal * tasa_cupon_periodo


def calcular_numero_periodos(años: int, frecuencia_anual: int) -> int:
    """
    Calcula el número total de periodos.
    
    Args:
        años: Años al vencimiento
        frecuencia_anual: Número de pagos por año
    
    Returns:
        Número total de periodos
    """
    return años * frecuencia_anual


def calcular_valor_presente_cupon(cupon: float, tasa_descuento: float, periodo: int) -> float:
    """
    Calcula el valor presente de un cupón específico.
    
    Args:
        cupon: Monto del cupón
        tasa_descuento: Tasa de descuento por periodo
        periodo: Número del periodo
    
    Returns:
        Valor presente del cupón
    """
    return cupon / ((1 + tasa_descuento) ** periodo)


def calcular_valor_presente_nominal(valor_nominal: float, tasa_descuento: float, num_periodos: int) -> float:
    """
    Calcula el valor presente del valor nominal.
    
    Args:
        valor_nominal: Valor nominal del bono
        tasa_descuento: Tasa de descuento por periodo
        num_periodos: Número total de periodos
    
    Returns:
        Valor presente del valor nominal
    """
    return valor_nominal / ((1 + tasa_descuento) ** num_periodos)


def calcular_valor_presente_bono(
    valor_nominal: float,
    tasa_cupon_anual: float,
    frecuencia_anual: int,
    años: int,
    tea_descuento: float
) -> dict:
    """
    Calcula el valor presente de un bono y genera el detalle de flujos.
    
    Args:
        valor_nominal: Valor nominal del bono
        tasa_cupon_anual: Tasa cupón anual (TEA) en decimal
        frecuencia_anual: Número de pagos por año
        años: Años al vencimiento
        tea_descuento: Tasa efectiva anual de descuento en decimal
    
    Returns:
        Diccionario con el valor presente y detalle de flujos
    """
    # Calcular tasas por periodo
    tasa_cupon_periodo = calcular_tasa_cupon_periodo(tasa_cupon_anual, frecuencia_anual)
    tasa_descuento_periodo = calcular_tasa_descuento_periodo(tea_descuento, frecuencia_anual)
    
    # Calcular cupón y número de periodos
    cupon = calcular_cupon(valor_nominal, tasa_cupon_periodo)
    num_periodos = calcular_numero_periodos(años, frecuencia_anual)
    
    # Calcular flujos y valores presentes
    flujos = []
    vp_total_cupones = 0
    
    for periodo in range(1, num_periodos + 1):
        # Flujo del periodo (cupón)
        flujo = cupon
        
        # En el último periodo, agregar el valor nominal
        if periodo == num_periodos:
            flujo += valor_nominal
        
        # Valor presente de este flujo
        vp_flujo = flujo / ((1 + tasa_descuento_periodo) ** periodo)
        
        flujos.append({
            'periodo': periodo,
            'flujo': flujo,
            'vp_flujo': vp_flujo,
            'es_ultimo': periodo == num_periodos
        })
        
        vp_total_cupones += vp_flujo
    
    return {
        'valor_presente_total': vp_total_cupones,
        'cupon_periodico': cupon,
        'num_periodos': num_periodos,
        'tasa_cupon_periodo': tasa_cupon_periodo,
        'tasa_descuento_periodo': tasa_descuento_periodo,
        'flujos': flujos
    }
