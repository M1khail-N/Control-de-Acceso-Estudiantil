from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profesor, Asignatura, Maquina, Alumno
from .serializers import ProfesorSerializer, AsignaturaSerializer, MaquinaSerializer, AlumnoSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer
    
    @action(detail=True, methods=['get'])
    def profesor(self, request, pk=None):
        asignatura = self.get_object()
        profesor = asignatura.profesor
        from micsv.svGestionRegistros.serializers import ProfesorSerializer
        return Response(ProfesorSerializer(profesor).data)


class MaquinaViewSet(viewsets.ModelViewSet):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer


class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer