def formatear_moneda(monto: float, moneda: str = "USD") -> str:
    """
    Formatea un monto como moneda.
    
    Args:
        monto: Monto a formatear
        moneda: Símbolo de la moneda
    
    Returns:
        String formateado
    """
    return f"{moneda} {monto:,.2f}"


def calcular_edad_jubilacion(edad_actual: int, plazo_años: int) -> int:
    """
    Calcula la edad de jubilación.
    
    Args:
        edad_actual: Edad actual
        plazo_años: Años hasta la jubilación
    
    Returns:
        Edad de jubilación
    """
    return edad_actual + plazo_años


def validar_datos_entrada(vp: float, aporte: float) -> tuple[bool, str]:
    """
    Valida que al menos uno de los valores de entrada sea mayor a 0.
    
    Args:
        vp: Valor Presente
        aporte: Aporte periódico
    
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if vp <= 0 and aporte <= 0:
        return False, "Debes ingresar al menos una inversión inicial o un aporte periódico."
    return True, ""
