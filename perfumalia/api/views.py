from rest_framework import generics 
from .serializers import PerfumeSerializer 
from store.models import Perfume 

class PerfumeList(generics.ListAPIView): 
    serializer_class = PerfumeSerializer 

    def get_queryset(self): 
        user = self.request.user 
        return Perfume.objects.order_by('-name')