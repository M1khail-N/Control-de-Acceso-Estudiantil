from rest_framework import serializers
from .models import Profesor, Asignatura, Maquina, Alumno


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'


class AsignaturaSerializer(serializers.ModelSerializer):
    nombre_profesor = serializers.CharField(source="profesor.nombre", read_only=True)
    apellido_profesor = serializers.CharField(source="profesor.apellido", read_only=True)

    class Meta:
        model = Asignatura
        fields = ["id_asignatura", "nombre", "profesor",
                  "nombre_profesor", "apellido_profesor"]


class MaquinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maquina
        fields = '__all__'


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'