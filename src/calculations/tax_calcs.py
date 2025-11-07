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


def calcular_retiro_mensual_con_impuestos(
    vf: float,
    beneficio_bruto: float,
    tasa_mensual_retiro: float,
    meses: int,
    tipo_bolsa: str
) -> dict:
    """
    Calcula el monto de retiro mensual considerando impuestos.
    
    IMPORTANTE: Para retiro mensual:
    - Base de cálculo: Valor Futuro completo (sin restar impuestos)
    - Impuesto fijo del 5% (independiente de bolsa nacional o extranjera)
    - Se aplica SOLO a los intereses generados mensualmente
    - TEA mensual: 50% de la TEA original
    
    Args:
        vf: Valor Futuro acumulado (base completa)
        beneficio_bruto: No se usa en este cálculo (mantenido por compatibilidad)
        tasa_mensual_retiro: Tasa mensual de retiro (50% de TEA original)
        meses: Número de meses de retiro
        tipo_bolsa: No afecta el cálculo (siempre 5% en retiro mensual)
    
    Returns:
        Diccionario con cálculos detallados de retiro mensual
    """
    # Impuesto fijo del 5% para retiros mensuales
    IMPUESTO_RETIRO_MENSUAL = 0.05
    
    # Simular retiros mes a mes para calcular impuestos sobre intereses
    saldo = vf
    total_retiro_bruto = 0
    total_impuestos = 0
    total_retiro_neto = 0
    
    # Calcular retiro mensual bruto (sin impuestos)
    if tasa_mensual_retiro == 0:
        retiro_mensual_bruto = vf / meses if meses > 0 else 0
    else:
        # Fórmula de anualidad: C = VP * [i / (1 - (1 + i)^-n)]
        retiro_mensual_bruto = vf * (tasa_mensual_retiro / (1 - (1 + tasa_mensual_retiro) ** -meses))
    
    # Simular cada mes para calcular intereses e impuestos
    for mes in range(meses):
        # Interés generado este mes sobre el saldo
        interes_mes = saldo * tasa_mensual_retiro
        
        # Impuesto del 5% sobre el interés generado
        impuesto_mes = interes_mes * IMPUESTO_RETIRO_MENSUAL
        
        # Capital que se retira (retiro - interés)
        capital_retirado = retiro_mensual_bruto - interes_mes
        
        # Retiro neto mensual (retiro bruto - impuesto sobre interés)
        retiro_neto_mes = retiro_mensual_bruto - impuesto_mes
        
        # Actualizar totales
        total_retiro_bruto += retiro_mensual_bruto
        total_impuestos += impuesto_mes
        total_retiro_neto += retiro_neto_mes
        
        # Actualizar saldo (saldo + interés - retiro bruto)
        saldo = saldo + interes_mes - retiro_mensual_bruto
        
        # Ajustar saldo si es el último mes (por redondeos)
        if mes == meses - 1 and abs(saldo) < 1:
            saldo = 0
    
    return {
        'impuesto': total_impuestos,
        'capital_neto': vf,  # Base completa para retiros mensuales
        'retiro_mensual': retiro_mensual_bruto - (total_impuestos / meses),  # Retiro neto promedio
        'retiro_mensual_bruto': retiro_mensual_bruto,
        'retiro_mensual_neto': retiro_mensual_bruto - (total_impuestos / meses),
        'total_retirado': total_retiro_neto,
        'total_impuestos_mensuales': total_impuestos
    }
