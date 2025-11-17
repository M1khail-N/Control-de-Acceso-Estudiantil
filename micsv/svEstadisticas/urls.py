from django.urls import path
from .views import (
    PromedioTiempoPorMotivo,
    AlumnosPorMaquinaAsignatura,
    CicloUsoLaboratorio,
    UsoSemanaOrdenado,
    DashboardGeneral
)

urlpatterns = [

    # 1. Tiempo promedio en minutos por motivo y mes
    path("motivo/promedio/", PromedioTiempoPorMotivo.as_view()),

    # 2. Estudiantes por máquina + asignatura + fecha
    path("maquina/consulta/", AlumnosPorMaquinaAsignatura.as_view()),

    # 3. Ciclo con más uso (dashboard)
    path("laboratorio/ciclo-uso/", CicloUsoLaboratorio.as_view()),

    # 4. Uso del laboratorio en una semana ordenado por edad
    path("laboratorio/uso-semana/", UsoSemanaOrdenado.as_view()),

    # 5. Dashboard unificado
    path("dashboard/resumen/", DashboardGeneral.as_view()),
]