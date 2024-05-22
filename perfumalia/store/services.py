from .interfaces import I_HTMLManager
from django.template.loader import get_template

class HTML_Service:
    def __init__(self, pdf_manager: I_HTMLManager):
        self.pdf_manager = pdf_manager

    def create_Check(self, datos: str):
        # Renderiza la plantilla HTML con los datos
        template_path = 'pdf_generator/plantilla_pdf.html'
        template = get_template(template_path)
        html = template.render(datos)

        response = self.pdf_manager.transform_html(html)
        return response