from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from .models import RegistroBase, RegistroLibre, RegistroClase
from micsv.svGestionRegistros.models import Alumno, Maquina, Asignatura, Profesor

from .serializers import (
    RegistroBaseSerializer,
    RegistroLibreSerializer,
    RegistroClaseSerializer
)

def crear_registro_base(codigo_alumno, maquina_id):
    try:
        alumno = Alumno.objects.get(codigo_alumno=codigo_alumno)
    except Alumno.DoesNotExist:
        return None, {"detail": "Alumno no encontrado."}, 404

    try:
        maquina = Maquina.objects.get(id_maquina=maquina_id)
    except Maquina.DoesNotExist:
        return None, {"detail": "Máquina no encontrada."}, 404

    # Verificar si ya existe registro abierto
    abierto = RegistroBase.objects.filter(
        alumno=alumno,
        fecha_hora_salida__isnull=True
    ).first()

    if abierto:
        return None, {
            "detail": "El alumno ya tiene una sesión abierta.",
            "registro_abierto": RegistroBaseSerializer(abierto).data
        }, 400

    reg_base = RegistroBase.objects.create(
        alumno=alumno,
        maquina=maquina,
        fecha_hora_entrada=timezone.now()
    )

    return reg_base, None, 201

class RegistroBaseViewSet(viewsets.ModelViewSet):
    queryset = RegistroBase.objects.all()
    serializer_class = RegistroBaseSerializer

    @action(detail=False, methods=["post"])
    def entrada(self, request):
        codigo_alumno = request.data.get("codigo_alumno")
        maquina_id = request.data.get("maquina_id")

        if not codigo_alumno or not maquina_id:
            return Response({"detail": "Faltan datos."}, status=400)

        reg, error, status_code = crear_registro_base(codigo_alumno, maquina_id)
        if error:
            return Response(error, status=status_code)

        return Response(RegistroBaseSerializer(reg).data, status=201)

    @action(detail=False, methods=["post"])
    def salida(self, request):
        codigo_alumno = request.data.get("codigo_alumno")

        if not codigo_alumno:
            return Response({"detail": "Debe enviar codigo_alumno."}, status=400)

        try:
            alumno = Alumno.objects.get(codigo_alumno=codigo_alumno)
        except Alumno.DoesNotExist:
            return Response({"detail": "Alumno no encontrado."}, status=404)

        registro = RegistroBase.objects.filter(
            alumno=alumno,
            fecha_hora_salida__isnull=True
        ).first()

        if not registro:
            return Response({"detail": "No hay registro abierto."}, status=404)

        registro.fecha_hora_salida = timezone.now()
        registro.save()

        return Response(RegistroBaseSerializer(registro).data)


# =============================================================
# REGISTRO LIBRE
# =============================================================
class RegistroLibreViewSet(viewsets.ModelViewSet):
    queryset = RegistroLibre.objects.all()
    serializer_class = RegistroLibreSerializer

    @action(detail=False, methods=['post'])
    def entrada(self, request):
        codigo_alumno = request.data.get("codigo_alumno")
        maquina_id = request.data.get("maquina_id")
        motivo = request.data.get("motivo")

        if not motivo:
            return Response({"detail": "Debe enviar motivo."}, status=400)

        reg_base, error, status_code = crear_registro_base(codigo_alumno, maquina_id)
        if error:
            return Response(error, status=status_code)

        libre = RegistroLibre.objects.create(
            reg_base=reg_base,
            motivo=motivo
        )

        return Response(RegistroLibreSerializer(libre).data, status=201)

# =============================================================
# REGISTRO DE CLASE
# =============================================================
class RegistroClaseViewSet(viewsets.ModelViewSet):
    queryset = RegistroClase.objects.all()
    serializer_class = RegistroClaseSerializer

    @action(detail=False, methods=['post'])
    def entrada(self, request):
        codigo_alumno = request.data.get("codigo_alumno")
        maquina_id = request.data.get("maquina_id")
        asignatura_id = request.data.get("asignatura_id")
        profesor_id = request.data.get("profesor_id")

        if not asignatura_id or not profesor_id:
            return Response({"detail": "Faltan asignatura_id o profesor_id."}, status=400)

        # Crear registro base
        reg_base, error, status_code = crear_registro_base(codigo_alumno, maquina_id)
        if error:
            return Response(error, status=status_code)

        # Buscar asignatura
        try:
            asignatura = Asignatura.objects.get(id_asignatura=asignatura_id)
        except Asignatura.DoesNotExist:
            return Response({"detail": "Asignatura no encontrada."}, status=404)

        # Buscar profesor
        try:
            profesor = Profesor.objects.get(id_profesor=profesor_id)
        except Profesor.DoesNotExist:
            return Response({"detail": "Profesor no encontrado."}, status=404)

        # Validación manual (opcional, ya la hace el serializer, pero aquí da mejor UX)
        if asignatura.profesor_id != profesor.id_profesor:
            return Response(
                {"detail": "El profesor no está asignado a esta asignatura."},
                status=400
            )

        clase = RegistroClase.objects.create(
            reg_base=reg_base,
            asignatura=asignatura,
            profesor=profesor
        )

        return Response(RegistroClaseSerializer(clase).data, status=201)