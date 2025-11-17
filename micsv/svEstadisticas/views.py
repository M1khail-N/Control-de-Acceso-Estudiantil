from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, F, ExpressionWrapper, DurationField, Count
from django.db.models.functions import ExtractWeek, ExtractYear
from datetime import date

from micsv.svRegAcceso.models import RegistroBase, RegistroLibre, RegistroClase
from micsv.svGestionRegistros.models import Alumno

from .serializers import (
    PromedioTiempoMotivoSerializer,
    AlumnosPorMaquinaAsignaturaSerializer,
    CicloUsoLaboratorioSerializer,
    UsoSemanaOrdenadoSerializer,
    DashboardGeneralSerializer,
    FiltroMesSerializer,
    FiltroMaquinaAsignaturaFechaSerializer,
    FiltroSemanaSerializer,
    FiltroCicloSerializer
)

# 1. Promedio de tiempo por motivo (mes específico)
class PromedioTiempoPorMotivo(APIView):

    def get(self, request):
        filtro = FiltroMesSerializer(data=request.GET)
        if not filtro.is_valid():
            return Response(filtro.errors, status=status.HTTP_400_BAD_REQUEST)

        mes = filtro.validated_data['mes']

        registros = RegistroLibre.objects.filter(
            reg_base__fecha_hora_entrada__month=mes,
            reg_base__fecha_hora_salida__isnull=False
        ).annotate(
            duracion=ExpressionWrapper(
                F("reg_base__fecha_hora_salida") - F("reg_base__fecha_hora_entrada"),
                output_field=DurationField()
            )
        ).values("motivo").annotate(
            promedio=Avg("duracion")
        ).order_by("motivo")

        data = [
            {"motivo": r["motivo"], "promedio_minutos": r["promedio"].total_seconds() / 60}
            for r in registros
        ]

        serializer = PromedioTiempoMotivoSerializer(data, many=True)
        return Response(serializer.data)

# 2. Listado de alumnos por máquina + asignatura + fecha
class AlumnosPorMaquinaAsignatura(APIView):

    def get(self, request):
        filtro = FiltroMaquinaAsignaturaFechaSerializer(data=request.GET)
        if not filtro.is_valid():
            return Response(filtro.errors, status=status.HTTP_400_BAD_REQUEST)

        maquina_id = filtro.validated_data['maquina_id']
        asignatura_id = filtro.validated_data['asignatura_id']
        fecha = filtro.validated_data['fecha']

        registros = RegistroClase.objects.filter(
            asignatura_id=asignatura_id,
            reg_base__maquina_id=maquina_id,
            reg_base__fecha_hora_entrada__date=fecha
        ).select_related("reg_base", "reg_base__alumno")

        data = [
            {
                "id_alumno": r.reg_base.alumno.id_alumno,
                "codigo_alumno": r.reg_base.alumno.codigo_alumno,
                "nombre": r.reg_base.alumno.nombre,
                "apellido": r.reg_base.alumno.apellido,
                "carrera": r.reg_base.alumno.carrera,
                "ciclo": r.reg_base.alumno.ciclo,
                "fecha_entrada": r.reg_base.fecha_hora_entrada,
                "fecha_salida": r.reg_base.fecha_hora_salida,
            }
            for r in registros
        ]

        serializer = AlumnosPorMaquinaAsignaturaSerializer(data, many=True)
        return Response(serializer.data)

# 3. Ciclo que más usa el laboratorio
class CicloUsoLaboratorio(APIView):

    def get(self, request):
        filtro = FiltroCicloSerializer(data=request.GET)
        if not filtro.is_valid():
            return Response(filtro.errors, status=status.HTTP_400_BAD_REQUEST)

        carrera = filtro.validated_data.get("carrera", None)

        registros = RegistroBase.objects.select_related("alumno")

        if carrera:
            registros = registros.filter(alumno__carrera=carrera)

        registros = registros.values(
            ciclo=F("alumno__ciclo")
        ).annotate(
            total=Count("id_reg_base")
        ).order_by("-total")

        serializer = CicloUsoLaboratorioSerializer(registros, many=True)
        return Response(serializer.data)

# 4. Uso del laboratorio por semana, ordenado por edad
class UsoSemanaOrdenado(APIView):

    def get(self, request):
        filtro = FiltroSemanaSerializer(data=request.GET)
        if not filtro.is_valid():
            return Response(filtro.errors, status=status.HTTP_400_BAD_REQUEST)

        semana = filtro.validated_data['semana']
        anio = filtro.validated_data['anio']

        registros = RegistroBase.objects.annotate(
            week=ExtractWeek('fecha_hora_entrada'),
            year=ExtractYear('fecha_hora_entrada')
        ).filter(
            week=semana,
            year=anio
        ).select_related("alumno")

        data = []
        for r in registros:
            alumno = r.alumno
            edad = calcular_edad(alumno.fecha_nacimiento)
            data.append({
                "id_alumno": alumno.id_alumno,
                "codigo_alumno": alumno.codigo_alumno,
                "nombre": alumno.nombre,
                "apellido": alumno.apellido,
                "edad": edad,
                "fecha_entrada": r.fecha_hora_entrada,
                "fecha_salida": r.fecha_hora_salida
            })

        data = sorted(data, key=lambda x: x["edad"])

        serializer = UsoSemanaOrdenadoSerializer(data, many=True)
        return Response(serializer.data)

# 5. Dashboard General
class DashboardGeneral(APIView):

    def get(self, request):
        # Sesiones activas
        total_activas = RegistroBase.objects.filter(
            fecha_hora_salida__isnull=True
        ).count()

        # Promedio tiempo en RegistroLibre
        promedio_tiempo = RegistroLibre.objects.annotate(
            duracion=ExpressionWrapper(
                F("reg_base__fecha_hora_salida") - F("reg_base__fecha_hora_entrada"),
                output_field=DurationField()
            )
        ).aggregate(
            promedio=Avg("duracion")
        )["promedio"]

        # Ciclo con más uso
        ciclo_top = RegistroBase.objects.values(
            ciclo=F("alumno__ciclo")
        ).annotate(
            total=Count("id_reg_base")
        ).order_by("-total").first()

        data = {
            "sesiones_activas": total_activas,
            "promedio_tiempo_minutos": promedio_tiempo.total_seconds() / 60 if promedio_tiempo else 0,
            "ciclo_con_mas_uso": ciclo_top["ciclo"] if ciclo_top else None,
            "total_sesiones_ciclo": ciclo_top["total"] if ciclo_top else 0,
        }

        serializer = DashboardGeneralSerializer(data)
        return Response(serializer.data)

# Función auxiliar para calcular edad
def calcular_edad(fecha_nac):
    today = date.today()
    return today.year - fecha_nac.year - (
        (today.month, today.day) < (fecha_nac.month, fecha_nac.day)
    )