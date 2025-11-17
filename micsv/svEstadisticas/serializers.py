from rest_framework import serializers

# Serializadores de filtros
class FiltroMesSerializer(serializers.Serializer):
    mes = serializers.IntegerField(min_value=1, max_value=12)

class FiltroMaquinaAsignaturaFechaSerializer(serializers.Serializer):
    maquina_id = serializers.IntegerField()
    asignatura_id = serializers.IntegerField()
    fecha = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])

class FiltroSemanaSerializer(serializers.Serializer):
    semana = serializers.IntegerField(min_value=1, max_value=53)
    anio = serializers.IntegerField(min_value=2000, max_value=2100)

class FiltroCicloSerializer(serializers.Serializer):
    carrera = serializers.CharField(required=False, allow_blank=True)

# Serializadores de resultados
class PromedioTiempoMotivoSerializer(serializers.Serializer):
    motivo = serializers.CharField(read_only=True)
    promedio_minutos = serializers.FloatField(read_only=True)

class AlumnosPorMaquinaAsignaturaSerializer(serializers.Serializer):
    id_alumno = serializers.IntegerField(read_only=True)
    codigo_alumno = serializers.CharField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    carrera = serializers.CharField(read_only=True)
    ciclo = serializers.IntegerField(read_only=True)
    fecha_entrada = serializers.DateTimeField(read_only=True)
    fecha_salida = serializers.DateTimeField(read_only=True)

class CicloUsoLaboratorioSerializer(serializers.Serializer):
    ciclo = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)

class UsoSemanaOrdenadoSerializer(serializers.Serializer):
    id_alumno = serializers.IntegerField(read_only=True)
    codigo_alumno = serializers.CharField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    edad = serializers.IntegerField(read_only=True)
    fecha_entrada = serializers.DateTimeField(read_only=True)
    fecha_salida = serializers.DateTimeField(read_only=True, allow_null=True)

class DashboardGeneralSerializer(serializers.Serializer):
    sesiones_activas = serializers.IntegerField(read_only=True)
    promedio_tiempo_minutos = serializers.FloatField(read_only=True)
    ciclo_con_mas_uso = serializers.IntegerField(allow_null=True, read_only=True)
    total_sesiones_ciclo = serializers.IntegerField(read_only=True)