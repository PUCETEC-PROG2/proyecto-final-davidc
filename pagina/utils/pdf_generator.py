from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from django.conf import settings
from datetime import datetime

def generar_contrato(compra):
    # Crear el directorio para contratos si no existe
    contratos_dir = os.path.join(settings.MEDIA_ROOT, 'contratos')
    if not os.path.exists(contratos_dir):
        os.makedirs(contratos_dir)
    
    # Nombre del archivo
    filename = f'contrato_compra_{compra.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    filepath = os.path.join(contratos_dir, filename)
    
    # Crear el documento
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Contenido del documento
    Story = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    Story.append(Paragraph("CONTRATO DE COMPRAVENTA", title_style))
    
    # Información de la compra
    Story.append(Paragraph(f"Fecha: {compra.fecha_compra.strftime('%d/%m/%Y')}", styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    # Información del cliente
    Story.append(Paragraph("DATOS DEL COMPRADOR:", styles["Heading2"]))
    Story.append(Paragraph(f"Nombre: {compra.cliente.primer_nombre} {compra.cliente.primer_apellido}", styles["Normal"]))
    Story.append(Paragraph(f"Cédula: {compra.cliente.cedula}", styles["Normal"]))
    Story.append(Paragraph(f"Dirección: {compra.cliente.direccion}", styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    # Información de las propiedades
    
    
    # Información del precio
    Story.append(Paragraph("INFORMACIÓN DE PAGO:", styles["Heading2"]))
    Story.append(Paragraph(f"Precio sin IVA: ${compra.precio_sin_iva}", styles["Normal"]))
    Story.append(Paragraph(f"Precio con IVA: ${compra.precio_con_iva}", styles["Normal"]))
    
    # Construir el PDF
    doc.build(Story)
    
    return filename