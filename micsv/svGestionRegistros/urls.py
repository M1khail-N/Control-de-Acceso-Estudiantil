from rest_framework import routers
from django.urls import path, include
from .views import (
    ProfesorViewSet,
    AsignaturaViewSet,
    MaquinaViewSet,
    AlumnoViewSet
)

router = routers.DefaultRouter()
router.register('profesores', ProfesorViewSet)
router.register('asignaturas', AsignaturaViewSet)
router.register('maquinas', MaquinaViewSet)
router.register('alumnos', AlumnoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]