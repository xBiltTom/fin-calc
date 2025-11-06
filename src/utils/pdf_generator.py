from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime
import plotly.graph_objects as go
import os


def crear_pdf_acciones(
    datos_entrada: dict,
    resultados_vf: dict,
    resultados_retiro: dict,
    tipo_retiro: str,
    df_tabla: object = None,
    fig_evolucion: go.Figure = None
) -> BytesIO:
    """
    Genera un PDF con los resultados de la calculadora de acciones.
    
    Args:
        datos_entrada: Datos ingresados por el usuario
        resultados_vf: Resultados del cálculo de valor futuro
        resultados_retiro: Resultados del cálculo de retiro
        tipo_retiro: "total" o "mensual"
        df_tabla: DataFrame con tabla de crecimiento (opcional)
        fig_evolucion: Figura de Plotly con gráfico (opcional)
    
    Returns:
        BytesIO con el PDF generado
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Título
    story.append(Paragraph("📈 Reporte de Inversión en Acciones", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Fecha de generación
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<i>Generado el: {fecha_actual}</i>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # 1. Datos de entrada
    story.append(Paragraph("📋 Datos de Entrada", heading_style))
    
    datos_tabla = [
        ['Campo', 'Valor'],
        ['Edad actual', f"{datos_entrada['edad_actual']} años"],
        ['Inversión inicial', f"USD {datos_entrada['valor_presente']:,.2f}"],
        ['Aporte periódico', f"USD {datos_entrada['aporte_periodico']:,.2f}"],
        ['Frecuencia', datos_entrada['frecuencia']],
        ['Plazo', f"{datos_entrada['plazo_años']} años"],
        ['Edad de jubilación', f"{datos_entrada['edad_actual'] + datos_entrada['plazo_años']} años"],
        ['TEA', f"{datos_entrada['tea_pct']:.2f}%"],
        ['Tipo de inversión', datos_entrada['tipo_bolsa']],
    ]
    
    tabla_datos = Table(datos_tabla, colWidths=[2.5*inch, 3*inch])
    tabla_datos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4ECDC4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 0.3*inch))
    
    # 2. Resultados del Valor Futuro
    story.append(Paragraph("💰 Valor Futuro de la Inversión", heading_style))
    
    vf_tabla = [
        ['Concepto', 'Monto (USD)'],
        ['Valor Futuro (VF)', f"{resultados_vf['vf']:,.2f}"],
        ['Inversión Total', f"{resultados_vf['inversion_total']:,.2f}"],
        ['Beneficio Bruto', f"{resultados_vf['beneficio_bruto']:,.2f}"],
        ['Rentabilidad', f"{(resultados_vf['beneficio_bruto']/resultados_vf['inversion_total']*100):.2f}%"],
    ]
    
    tabla_vf = Table(vf_tabla, colWidths=[2.5*inch, 3*inch])
    tabla_vf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(tabla_vf)
    story.append(Spacer(1, 0.3*inch))
    
    # 3. Resultados de retiro
    if tipo_retiro == "total":
        story.append(Paragraph("🏦 Retiro Total", heading_style))
        
        tasa_impuesto = "5%" if datos_entrada['tipo_bolsa'] == "Nacional" else "29.5%"
        
        retiro_tabla = [
            ['Concepto', 'Monto (USD)'],
            ['Valor Futuro', f"{resultados_retiro['vf']:,.2f}"],
            [f'Impuesto ({tasa_impuesto})', f"{resultados_retiro['impuesto']:,.2f}"],
            ['Monto Neto a Recibir', f"{resultados_retiro['monto_neto']:,.2f}"],
        ]
        
        tabla_retiro = Table(retiro_tabla, colWidths=[2.5*inch, 3*inch])
        tabla_retiro.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7f0e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgoldenrodyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(tabla_retiro)
        
    else:  # retiro mensual
        story.append(Paragraph("💳 Retiros Mensuales", heading_style))
        
        tasa_impuesto = "5%" if datos_entrada['tipo_bolsa'] == "Nacional" else "29.5%"
        
        retiro_tabla = [
            ['Concepto', 'Valor'],
            ['Valor Futuro', f"USD {resultados_retiro['vf']:,.2f}"],
            [f'Impuesto ({tasa_impuesto})', f"USD {resultados_retiro['impuesto']:,.2f}"],
            ['Capital Neto Disponible', f"USD {resultados_retiro['capital_neto']:,.2f}"],
            ['Retiro Mensual', f"USD {resultados_retiro['retiro_mensual']:,.2f}"],
            ['Periodo de retiro', f"{resultados_retiro['meses']} meses ({resultados_retiro['meses']/12:.1f} años)"],
            ['Total a Retirar', f"USD {resultados_retiro['total_retirado']:,.2f}"],
        ]
        
        tabla_retiro = Table(retiro_tabla, colWidths=[2.5*inch, 3*inch])
        tabla_retiro.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7f0e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgoldenrodyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(tabla_retiro)
    
    story.append(Spacer(1, 0.3*inch))
    
    # 4. Tabla de crecimiento (si está disponible)
    if df_tabla is not None and len(df_tabla) > 0:
        story.append(PageBreak())
        story.append(Paragraph("📊 Tabla de Crecimiento Detallada", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Mostrar solo primeros 30 periodos en el PDF
        df_mostrar = df_tabla.head(30) if len(df_tabla) > 30 else df_tabla
        
        # Preparar datos para la tabla
        tabla_data = [['Periodo', 'Saldo Inicial', 'Aporte', 'Interés', 'Saldo Final']]
        
        for _, row in df_mostrar.iterrows():
            tabla_data.append([
                str(int(row['Periodo'])),
                f"{row['Saldo Inicial (USD)']:,.2f}",
                f"{row['Aporte (USD)']:,.2f}",
                f"{row['Interés Ganado (USD)']:,.2f}",
                f"{row['Saldo Final (USD)']:,.2f}"
            ])
        
        tabla_crecimiento = Table(tabla_data, colWidths=[0.8*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        tabla_crecimiento.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.95, 0.95, 0.95)),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        story.append(tabla_crecimiento)
        
        if len(df_tabla) > 30:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"<i>Nota: Se muestran los primeros 30 periodos de {len(df_tabla)} totales.</i>",
                styles['Normal']
            ))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>Este reporte es generado automáticamente con fines informativos y educativos. "
        "No constituye asesoría financiera profesional.</i>",
        styles['Normal']
    ))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def crear_pdf_bonos(
    datos_entrada: dict,
    resultados: dict,
    df_flujos: object = None
) -> BytesIO:
    """
    Genera un PDF con los resultados de la calculadora de bonos.
    
    Args:
        datos_entrada: Datos ingresados por el usuario
        resultados: Resultados del cálculo de valoración
        df_flujos: DataFrame con flujos del bono (opcional)
    
    Returns:
        BytesIO con el PDF generado
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#9467bd'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Título
    story.append(Paragraph("📊 Reporte de Valoración de Bonos", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Fecha de generación
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<i>Generado el: {fecha_actual}</i>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # 1. Características del Bono
    story.append(Paragraph("📋 Características del Bono", heading_style))
    
    datos_tabla = [
        ['Característica', 'Valor'],
        ['Valor Nominal', f"USD {datos_entrada['valor_nominal']:,.2f}"],
        ['Tasa Cupón (TEA)', f"{datos_entrada['tasa_cupon_pct']:.2f}%"],
        ['Frecuencia de Pago', datos_entrada['frecuencia']],
        ['Plazo', f"{datos_entrada['plazo_años']} años"],
        ['Tasa de Retorno Esperada (TEA)', f"{datos_entrada['tea_descuento_pct']:.2f}%"],
        ['Número de Pagos', f"{resultados['num_periodos']}"],
        ['Cupón Periódico', f"USD {resultados['cupon_periodico']:,.2f}"],
    ]
    
    tabla_datos = Table(datos_tabla, colWidths=[2.5*inch, 3*inch])
    tabla_datos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9467bd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 0.3*inch))
    
    # 2. Resultados de la Valoración
    story.append(Paragraph("💰 Valoración del Bono", heading_style))
    
    vp_nominal = datos_entrada['valor_nominal']
    vp_total = resultados['valor_presente_total']
    diferencia = vp_total - vp_nominal
    porcentaje = (diferencia / vp_nominal) * 100
    
    if vp_total > vp_nominal:
        tipo_cotizacion = f"Bono con Prima (+{porcentaje:.2f}%)"
    elif vp_total < vp_nominal:
        tipo_cotizacion = f"Bono con Descuento ({porcentaje:.2f}%)"
    else:
        tipo_cotizacion = "Bono a la Par"
    
    valoracion_tabla = [
        ['Concepto', 'Valor'],
        ['Valor Presente del Bono', f"USD {resultados['valor_presente_total']:,.2f}"],
        ['Valor Nominal', f"USD {vp_nominal:,.2f}"],
        ['Diferencia', f"USD {diferencia:,.2f}"],
        ['Tipo de Cotización', tipo_cotizacion],
        ['Total en Cupones', f"USD {resultados['cupon_periodico'] * resultados['num_periodos']:,.2f}"],
    ]
    
    tabla_valoracion = Table(valoracion_tabla, colWidths=[2.5*inch, 3*inch])
    tabla_valoracion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(tabla_valoracion)
    story.append(Spacer(1, 0.3*inch))
    
    # 3. Tasas Efectivas
    story.append(Paragraph("📊 Tasas Efectivas por Periodo", heading_style))
    
    tasas_tabla = [
        ['Concepto', 'Tasa'],
        ['Tasa Cupón por Periodo', f"{resultados['tasa_cupon_periodo']*100:.4f}%"],
        ['Tasa Descuento por Periodo', f"{resultados['tasa_descuento_periodo']*100:.4f}%"],
    ]
    
    tabla_tasas = Table(tasas_tabla, colWidths=[3*inch, 2.5*inch])
    tabla_tasas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(tabla_tasas)
    story.append(Spacer(1, 0.3*inch))
    
    # 4. Tabla de Flujos (si está disponible)
    if df_flujos is not None and len(df_flujos) > 0:
        story.append(PageBreak())
        story.append(Paragraph("📋 Flujos de Caja del Bono", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Mostrar todos los flujos (o primeros 40 si hay muchos)
        df_mostrar = df_flujos.head(40) if len(df_flujos) > 40 else df_flujos
        
        # Preparar datos para la tabla
        tabla_data = [['Periodo', 'Flujo (USD)', 'Valor Presente (USD)', 'Tipo']]
        
        for _, row in df_mostrar.iterrows():
            flujo = row['Flujo (USD)'].replace(',', '') if isinstance(row['Flujo (USD)'], str) else row['Flujo (USD)']
            vp_flujo = row['Valor Presente (USD)'].replace(',', '') if isinstance(row['Valor Presente (USD)'], str) else row['Valor Presente (USD)']
            
            tabla_data.append([
                str(row['Periodo']),
                flujo if isinstance(flujo, str) else f"{flujo:,.2f}",
                vp_flujo if isinstance(vp_flujo, str) else f"{vp_flujo:,.2f}",
                row['Tipo']
            ])
        
        tabla_flujos = Table(tabla_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 2*inch])
        tabla_flujos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.95, 0.95, 0.95)),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        story.append(tabla_flujos)
        
        if len(df_flujos) > 40:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"<i>Nota: Se muestran los primeros 40 periodos de {len(df_flujos)} totales.</i>",
                styles['Normal']
            ))
    
    # Footer
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>Este reporte es generado automáticamente con fines informativos y educativos. "
        "No constituye asesoría financiera profesional.</i>",
        styles['Normal']
    ))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
