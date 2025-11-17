from rest_framework import routers
from django.urls import path, include
from .views import RegistroBaseViewSet, RegistroLibreViewSet, RegistroClaseViewSet

router = routers.DefaultRouter()
router.register('registro-base', RegistroBaseViewSet)
router.register('registro-libre', RegistroLibreViewSet)
router.register('registro-clase', RegistroClaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]