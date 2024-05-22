from abc import ABC, abstractmethod

from django.http import HttpResponse
from xhtml2pdf import pisa

from html2docx import html2docx
from io import BytesIO

class I_HTMLManager(ABC):
    @abstractmethod
    def transform_html(self, html):
        pass

class PDFManager(I_HTMLManager):
    def transform_html(self, html):
        # Crea un objeto HttpResponse con el contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cheque_de_pago.pdf"'

        # Convierte el HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response
    
class HTMLManager:
    def transform_html(self, html):
        # Preparar la respuesta HTTP con el HTML adjunto
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="cheque_de_pago.html"'
        return response