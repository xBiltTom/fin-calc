"""Script de prueba completo para cronograma de retiros - varios escenarios"""
from src.utils.tables import generar_cronograma_retiros, generar_resumen_cronograma_retiros
from src.calculations.tax_calcs import calcular_tasa_mensual_retiro

escenarios = [
    {"nombre": "Corto plazo (1 año)", "vf": 54385.72, "tea": 0.10, "meses": 12},
    {"nombre": "Mediano plazo (5 años)", "vf": 100000.00, "tea": 0.10, "meses": 60},
    {"nombre": "Largo plazo (20 años)", "vf": 200000.00, "tea": 0.10, "meses": 240},
]

print("=" * 100)
print("PRUEBA DE CRONOGRAMAS DE RETIRO - MÚLTIPLES ESCENARIOS")
print("=" * 100)

for i, escenario in enumerate(escenarios, 1):
    print(f"\n{'=' * 100}")
    print(f"ESCENARIO {i}: {escenario['nombre']}")
    print("=" * 100)
    
    vf = escenario['vf']
    tea = escenario['tea']
    meses = escenario['meses']
    
    tasa_mensual = calcular_tasa_mensual_retiro(tea)
    
    print(f"\nParámetros:")
    print(f"  Valor Futuro: ${vf:,.2f}")
    print(f"  TEA: {tea*100:.2f}%")
    print(f"  Tasa mensual: {tasa_mensual*100:.4f}%")
    print(f"  Periodo: {meses} meses ({meses/12:.1f} años)")
    
    # Generar cronograma
    df = generar_cronograma_retiros(vf, tasa_mensual, meses, "USD")
    resumen = generar_resumen_cronograma_retiros(df, "USD")
    
    print(f"\nResumen:")
    print(f"  Saldo Inicial: ${resumen['saldo_inicial']:,.2f}")
    print(f"  Total Intereses: ${resumen['total_intereses']:,.2f}")
    print(f"  Total Impuestos (5%): ${resumen['total_impuestos']:,.2f}")
    print(f"  Total Retiro Neto: ${resumen['total_retiro_neto']:,.2f}")
    print(f"  Retiro Mensual Promedio: ${resumen['retiro_mensual_promedio']:,.2f}")
    
    # Mostrar primeros 3 y últimos 3 meses
    print(f"\n  Primeros 3 meses:")
    for idx in range(min(3, len(df))):
        row = df.iloc[idx]
        print(f"    Mes {int(row['Mes']):3d}: Saldo ${row['Saldo Inicial (USD)']:10,.2f} | "
              f"Interés ${row['Interés Generado (USD)']:8,.2f} | "
              f"Impuesto ${row['Impuesto 5% (USD)']:7,.2f} | "
              f"Retiro Neto ${row['Retiro Neto (USD)']:8,.2f}")
    
    if len(df) > 6:
        print(f"    ... ({len(df) - 6} meses omitidos) ...")
    
    print(f"\n  Últimos 3 meses:")
    for idx in range(max(0, len(df) - 3), len(df)):
        row = df.iloc[idx]
        print(f"    Mes {int(row['Mes']):3d}: Saldo ${row['Saldo Inicial (USD)']:10,.2f} | "
              f"Interés ${row['Interés Generado (USD)']:8,.2f} | "
              f"Impuesto ${row['Impuesto 5% (USD)']:7,.2f} | "
              f"Retiro Neto ${row['Retiro Neto (USD)']:8,.2f}")
    
    # Validaciones
    saldo_final = df.iloc[-1]['Saldo Final (USD)']
    if abs(saldo_final) < 1:
        print(f"\n  ✅ Saldo final: ${saldo_final:.2f} (correcto)")
    else:
        print(f"\n  ⚠️  Saldo final: ${saldo_final:.2f} (debería ser ~0)")
    
    # Calcular ganancia neta durante el periodo de retiro
    ganancia_neta = resumen['total_retiro_neto'] - vf
    print(f"  💰 Ganancia neta por intereses: ${ganancia_neta:,.2f} ({(ganancia_neta/vf)*100:.2f}% del VF)")

print("\n" + "=" * 100)
print("COMPARACIÓN DE ESCENARIOS")
print("=" * 100)

print(f"\n{'Escenario':<30} {'VF Inicial':>15} {'Meses':>8} {'Retiro/mes':>15} {'Total Neto':>15} {'Ganancia':>15}")
print("-" * 100)

for escenario in escenarios:
    vf = escenario['vf']
    tea = escenario['tea']
    meses = escenario['meses']
    tasa_mensual = calcular_tasa_mensual_retiro(tea)
    
    df = generar_cronograma_retiros(vf, tasa_mensual, meses, "USD")
    resumen = generar_resumen_cronograma_retiros(df, "USD")
    
    ganancia = resumen['total_retiro_neto'] - vf
    
    print(f"{escenario['nombre']:<30} ${vf:>13,.2f} {meses:>8d} ${resumen['retiro_mensual_promedio']:>13,.2f} "
          f"${resumen['total_retiro_neto']:>13,.2f} ${ganancia:>13,.2f}")

print("\n✅ Todas las pruebas completadas!")
