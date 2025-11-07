"""Script de prueba para el cronograma de retiros mensuales"""
from src.utils.tables import generar_cronograma_retiros, generar_resumen_cronograma_retiros
from src.calculations.tax_calcs import calcular_tasa_mensual_retiro

# Parámetros de prueba
vf = 54385.72
tea = 0.10
meses = 12  # 1 año para ver los detalles

print("=" * 90)
print("CRONOGRAMA DE RETIROS MENSUALES")
print("=" * 90)

print(f"\nParámetros:")
print(f"  Valor Futuro: ${vf:,.2f}")
print(f"  TEA Original: {tea*100:.2f}%")
print(f"  Periodo de retiro: {meses} meses ({meses/12:.1f} año)")

tasa_mensual = calcular_tasa_mensual_retiro(tea)
print(f"  Tasa mensual de retiro: {tasa_mensual*100:.4f}% (50% de TEA)")

# Generar cronograma
df = generar_cronograma_retiros(vf, tasa_mensual, meses, "USD")
resumen = generar_resumen_cronograma_retiros(df, "USD")

print("\n" + "=" * 90)
print("RESUMEN DEL CRONOGRAMA")
print("=" * 90)
print(f"  Saldo Inicial: ${resumen['saldo_inicial']:,.2f}")
print(f"  Total Intereses Generados: ${resumen['total_intereses']:,.2f}")
print(f"  Total Impuestos (5%): ${resumen['total_impuestos']:,.2f}")
print(f"  Total Retiro Bruto: ${resumen['total_retiro_bruto']:,.2f}")
print(f"  Total Retiro Neto: ${resumen['total_retiro_neto']:,.2f}")
print(f"  Retiro Mensual Promedio: ${resumen['retiro_mensual_promedio']:,.2f}")

print("\n" + "=" * 90)
print("DETALLE MES A MES")
print("=" * 90)
print(df.to_string(index=False))

print("\n" + "=" * 90)
print("VALIDACIÓN")
print("=" * 90)

# Verificar que el saldo final sea cercano a 0
saldo_final = df.iloc[-1]['Saldo Final (USD)']
print(f"  Saldo final: ${saldo_final:,.2f}")
if abs(saldo_final) < 1:
    print("  ✅ El saldo final es aproximadamente 0 (correcto)")
else:
    print(f"  ⚠️  El saldo final debería ser 0")

# Verificar que impuestos = 5% de intereses
impuestos_esperados = resumen['total_intereses'] * 0.05
diferencia_impuestos = abs(resumen['total_impuestos'] - impuestos_esperados)
print(f"\n  Impuestos calculados: ${resumen['total_impuestos']:,.2f}")
print(f"  Impuestos esperados (5% de intereses): ${impuestos_esperados:,.2f}")
if diferencia_impuestos < 0.01:
    print("  ✅ Los impuestos son el 5% de los intereses (correcto)")
else:
    print(f"  ⚠️  Diferencia: ${diferencia_impuestos:,.2f}")

print("\n✅ Prueba completada!")
