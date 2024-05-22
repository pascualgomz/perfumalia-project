from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

class PDFManager:
    def create_pdf_from_html(self, html):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cheque_de_pago.pdf"'
        
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class PDF_Service:
    def __init__(self, pdf_manager):
        self.pdf_manager = pdf_manager

    def create_Check(self, datos):
        # Renderiza la plantilla HTML con los datos
        template_path = 'pdf_generator/plantilla_pdf.html'
        template = get_template(template_path)
        html = template.render(datos)

        response = self.pdf_manager.create_pdf_from_html(html)
        return response
