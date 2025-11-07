"""Script de prueba para verificar el nuevo cálculo de retiro mensual"""
from src.calculations.financial_calcs import calcular_vf_combinado, calcular_beneficio_bruto
from src.calculations.tax_calcs import (
    calcular_tasa_mensual_retiro,
    calcular_retiro_mensual_con_impuestos,
    calcular_impuesto_retiro_total,
    calcular_monto_neto_retiro_total
)

# Parámetros de prueba
vp = 10000
aporte = 500
tea = 0.10
frecuencia_anual = 12
plazo_años = 5
meses_retiro = 240  # 20 años

print("=" * 80)
print("PRUEBA DE RETIRO MENSUAL CON NUEVO CÁLCULO DE IMPUESTOS")
print("=" * 80)

print(f"\nParámetros de inversión:")
print(f"  Valor Presente: ${vp:,.2f}")
print(f"  Aporte Periódico: ${aporte:,.2f}")
print(f"  TEA: {tea*100:.2f}%")
print(f"  Frecuencia: {frecuencia_anual} veces/año")
print(f"  Plazo: {plazo_años} años")

# Calcular VF
vf = calcular_vf_combinado(vp, aporte, tea, frecuencia_anual, plazo_años, False)
total_aportes = aporte * frecuencia_anual * plazo_años
inversion_total = vp + total_aportes
beneficio_bruto = calcular_beneficio_bruto(vf, inversion_total)

print(f"\nResultados de acumulación:")
print(f"  Valor Futuro: ${vf:,.2f}")
print(f"  Inversión Total: ${inversion_total:,.2f}")
print(f"  Beneficio Bruto: ${beneficio_bruto:,.2f}")

print("\n" + "=" * 80)
print("OPCIÓN 1: RETIRO TOTAL")
print("=" * 80)

# Retiro total - Nacional
impuesto_total_nacional = calcular_impuesto_retiro_total(beneficio_bruto, "Nacional")
monto_neto_nacional = calcular_monto_neto_retiro_total(vf, impuesto_total_nacional)

print(f"\nBolsa Nacional (5%):")
print(f"  Impuesto sobre ganancia: ${impuesto_total_nacional:,.2f}")
print(f"  Monto neto a recibir: ${monto_neto_nacional:,.2f}")

# Retiro total - Extranjera
impuesto_total_extranjera = calcular_impuesto_retiro_total(beneficio_bruto, "Extranjera")
monto_neto_extranjera = calcular_monto_neto_retiro_total(vf, impuesto_total_extranjera)

print(f"\nBolsa Extranjera (29.5%):")
print(f"  Impuesto sobre ganancia: ${impuesto_total_extranjera:,.2f}")
print(f"  Monto neto a recibir: ${monto_neto_extranjera:,.2f}")

print("\n" + "=" * 80)
print("OPCIÓN 2: RETIRO MENSUAL")
print("=" * 80)

tasa_mensual_retiro = calcular_tasa_mensual_retiro(tea)
print(f"\nTasa mensual de retiro: {tasa_mensual_retiro*100:.4f}% (50% de TEA)")
print(f"Periodo de retiro: {meses_retiro} meses ({meses_retiro/12:.1f} años)")

# IMPORTANTE: El tipo de bolsa no afecta en retiro mensual (siempre 5%)
resultado_mensual = calcular_retiro_mensual_con_impuestos(
    vf=vf,
    beneficio_bruto=beneficio_bruto,
    tasa_mensual_retiro=tasa_mensual_retiro,
    meses=meses_retiro,
    tipo_bolsa="Nacional"  # No importa, siempre es 5%
)

print(f"\nResultados (independiente de tipo de bolsa):")
print(f"  Base de cálculo (VF): ${resultado_mensual['capital_neto']:,.2f}")
print(f"  Retiro mensual BRUTO: ${resultado_mensual.get('retiro_mensual_bruto', 0):,.2f}")
print(f"  Impuestos sobre intereses (5%): ${resultado_mensual['impuesto']:,.2f}")
print(f"  Retiro mensual NETO: ${resultado_mensual['retiro_mensual']:,.2f}")
print(f"  Total neto a retirar: ${resultado_mensual['total_retirado']:,.2f}")

print("\n" + "=" * 80)
print("COMPARACIÓN DE OPCIONES")
print("=" * 80)

print(f"\n1. Retiro Total Nacional:")
print(f"   Recibes de inmediato: ${monto_neto_nacional:,.2f}")

print(f"\n2. Retiro Total Extranjera:")
print(f"   Recibes de inmediato: ${monto_neto_extranjera:,.2f}")

print(f"\n3. Retiro Mensual (cualquier bolsa):")
print(f"   Recibes mensualmente: ${resultado_mensual['retiro_mensual']:,.2f}")
print(f"   Total neto en {meses_retiro/12:.1f} años: ${resultado_mensual['total_retirado']:,.2f}")
print(f"   Diferencia vs VF: ${resultado_mensual['total_retirado'] - vf:,.2f}")

print("\n" + "=" * 80)
print("ANÁLISIS")
print("=" * 80)

print(f"\n✅ Retiro total:")
print(f"   - Impuesto depende del tipo de bolsa (5% o 29.5%)")
print(f"   - Se aplica sobre la ganancia total")
print(f"   - Recibes todo de inmediato")

print(f"\n✅ Retiro mensual:")
print(f"   - Impuesto SIEMPRE es 5% (no importa tipo de bolsa)")
print(f"   - Se aplica SOLO a intereses generados cada mes")
print(f"   - Base de cálculo es el VF completo (${vf:,.2f})")
print(f"   - Total retirado puede ser > VF por intereses durante retiro")

print("\n✅ Prueba completada!")
