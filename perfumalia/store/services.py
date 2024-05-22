from .interfaces import I_PDFManager
from django.template.loader import get_template

class PDF_Service:
    def __init__(self, pdf_manager: I_PDFManager):
        self.pdf_manager = pdf_manager

    def create_Check(self, datos: str):
        # Renderiza la plantilla HTML con los datos
        template_path = 'pdf_generator/plantilla_pdf.html'
        template = get_template(template_path)
        html = template.render(datos)

        response = self.pdf_manager.create_pdf_from_html(html)
        return response