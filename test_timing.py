"""Script de prueba para verificar la inconsistencia de timing de aportes"""
from src.calculations.financial_calcs import calcular_vf_combinado
from src.utils.tables import generar_tabla_crecimiento

# Parámetros de prueba
vp = 10000
aporte = 500
tea = 0.10
frecuencia_anual = 12
plazo_años = 5

print("=" * 60)
print("PRUEBA DE TIMING DE APORTES")
print("=" * 60)
print(f"\nParámetros:")
print(f"  Valor Presente: ${vp:,.2f}")
print(f"  Aporte Periódico: ${aporte:,.2f}")
print(f"  TEA: {tea*100:.2f}%")
print(f"  Frecuencia: {frecuencia_anual} veces/año")
print(f"  Plazo: {plazo_años} años")

print("\n" + "=" * 60)
print("APORTE AL FINAL DEL PERIODO (Anualidad Vencida)")
print("=" * 60)

vf_vencida = calcular_vf_combinado(vp, aporte, tea, frecuencia_anual, plazo_años, False)
tabla_vencida = generar_tabla_crecimiento(vp, aporte, tea, frecuencia_anual, plazo_años, "USD", False)

print(f"\nValor Futuro (fórmula): ${vf_vencida:,.2f}")
print(f"Saldo Final (tabla): ${tabla_vencida.iloc[-1]['Saldo Final (USD)']:,.2f}")
print(f"Diferencia: ${abs(vf_vencida - tabla_vencida.iloc[-1]['Saldo Final (USD)']):,.2f}")

print("\n" + "=" * 60)
print("APORTE AL INICIO DEL PERIODO (Anualidad Anticipada)")
print("=" * 60)

vf_anticipada = calcular_vf_combinado(vp, aporte, tea, frecuencia_anual, plazo_años, True)
tabla_anticipada = generar_tabla_crecimiento(vp, aporte, tea, frecuencia_anual, plazo_años, "USD", True)

print(f"\nValor Futuro (fórmula): ${vf_anticipada:,.2f}")
print(f"Saldo Final (tabla): ${tabla_anticipada.iloc[-1]['Saldo Final (USD)']:,.2f}")
print(f"Diferencia: ${abs(vf_anticipada - tabla_anticipada.iloc[-1]['Saldo Final (USD)']):,.2f}")

print("\n" + "=" * 60)
print("COMPARACIÓN")
print("=" * 60)
print(f"\nDiferencia VF (anticipada vs vencida): ${vf_anticipada - vf_vencida:,.2f}")
print(f"Porcentaje: {((vf_anticipada/vf_vencida - 1) * 100):.2f}%")

print("\n✅ Prueba completada!")
