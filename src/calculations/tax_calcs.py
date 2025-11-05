from config.constants import IMPUESTO_BOLSA_NACIONAL, IMPUESTO_BOLSA_EXTRANJERA


def calcular_impuesto_retiro_total(beneficio_bruto: float, tipo_bolsa: str) -> float:
    """
    Calcula el impuesto sobre el beneficio bruto en un retiro total.
    
    Args:
        beneficio_bruto: Ganancia antes de impuestos (VF - Inversión Total)
        tipo_bolsa: "Nacional" o "Extranjera"
    
    Returns:
        Monto de impuesto a pagar
    """
    if beneficio_bruto <= 0:
        return 0
    
    tasa_impuesto = IMPUESTO_BOLSA_NACIONAL if tipo_bolsa == "Nacional" else IMPUESTO_BOLSA_EXTRANJERA
    return beneficio_bruto * tasa_impuesto


def calcular_monto_neto_retiro_total(vf: float, impuesto: float) -> float:
    """
    Calcula el monto neto después de impuestos en un retiro total.
    
    Args:
        vf: Valor Futuro
        impuesto: Monto de impuesto calculado
    
    Returns:
        Monto neto a recibir
    """
    return vf - impuesto


def calcular_tasa_mensual_retiro(tea: float) -> float:
    """
    Calcula la nueva tasa mensual para retiros mensuales.
    Según la especificación: nuevaTasaMensual = (1/2) × TEA
    
    Args:
        tea: Tasa Efectiva Anual (en decimal)
    
    Returns:
        Tasa mensual para retiros
    """
    return (1/2) * tea


def calcular_retiro_mensual(vf: float, tasa_mensual_retiro: float, meses: int) -> float:
    """
    Calcula el monto de retiro mensual basado en el VF y una tasa de retiro.
    
    Args:
        vf: Valor Futuro acumulado
        tasa_mensual_retiro: Tasa mensual de retiro
        meses: Número de meses de retiro
    
    Returns:
        Monto de retiro mensual
    """
    if tasa_mensual_retiro == 0:
        return vf / meses if meses > 0 else 0
    
    # Fórmula de anualidad: VP = C * [(1 - (1 + i)^-n) / i]
    # Despejando C: C = VP * [i / (1 - (1 + i)^-n)]
    return vf * (tasa_mensual_retiro / (1 - (1 + tasa_mensual_retiro) ** -meses))
