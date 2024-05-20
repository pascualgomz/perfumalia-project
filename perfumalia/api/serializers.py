from rest_framework import serializers 
from store.models import Perfume 

class PerfumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfume
        fields = '__all__'  # Incluye todos los campos del modelo Perfume