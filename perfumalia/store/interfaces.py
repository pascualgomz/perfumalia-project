from abc import ABC, abstractmethod

from django.http import HttpResponse
from xhtml2pdf import pisa

class I_PDFManager(ABC):
    @abstractmethod
    def create_pdf_from_html(self, html):
        pass

class PDFManager(I_PDFManager):
    def create_pdf_from_html(self, html):
        # Crea un objeto HttpResponse con el contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ejemplo.pdf"'

        # Convierte el HTML a PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response