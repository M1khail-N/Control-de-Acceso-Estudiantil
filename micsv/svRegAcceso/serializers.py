from rest_framework import serializers
from .models import RegistroBase, RegistroLibre, RegistroClase


class RegistroBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroBase
        fields = '__all__'


class RegistroLibreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroLibre
        fields = '__all__'


class RegistroClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroClase
        fields = '__all__'
    
    def validate(self, data):
        asignatura = data['asignatura']
        profesor = data['profesor']

        # Validación: la asignatura debe pertenecer al profesor seleccionado
        if asignatura.profesor != profesor:
            raise serializers.ValidationError(
                "El profesor seleccionado no dicta esta asignatura."
            )

        return data