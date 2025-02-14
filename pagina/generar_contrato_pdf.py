from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image  
from django.conf import settings  # Importa settings

def generar_contrato_pdf(compra, propiedades):
    # Create the canvas object
    c = canvas.Canvas(f"contrato_{compra.id}.pdf", pagesize=letter)
    
    # Set font and size
    c.setFont("Helvetica", 12)
    
    # Add title
    c.drawString(100, 750, "Contrato de Compraventa de Inmueble")
    
    # Add logo
    try:
        logo_path = settings.MEDIA_ROOT / "logocontrato" / "logocontrato.png"
        logo = Image(str(logo_path), width=100, height=100)
        logo.drawOn(c, 50, 700)
    except Exception as e:
        print(f"Error al cargar el logo: {e}")
    
    # Add purchase data
    y_position = 650
    c.drawString(100, y_position, f"ID de la Compra: {compra.id}")
    y_position -= 20
    c.drawString(100, y_position, f"Fecha de Compra: {compra.fecha_compra.strftime('%Y-%m-%d')}")
    y_position -= 20
    c.drawString(100, y_position, f"Cliente: {compra.cliente.primer_nombre} {compra.cliente.primer_apellido}")
    y_position -= 40
    
    # Add properties section
    c.drawString(100, y_position, "Propiedades adquiridas:")
    y_position -= 20
    
    # List all selected properties
    for propiedad in propiedades:
        c.drawString(120, y_position, f"- {propiedad.nombre}: ${propiedad.precio}")
        y_position -= 20
    
    # Add total prices
    y_position -= 20
    c.drawString(100, y_position, f"Total sin IVA: ${compra.precio_sin_iva}")
    y_position -= 20
    c.drawString(100, y_position, f"Total con IVA: ${compra.precio_con_iva}")
    
    # Save the PDF
    c.save()
    
