"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API basada en modulos
    path('api/gestion/', include('micsv.svGestionRegistros.urls')),
    path('api/acceso/', include('micsv.svRegAcceso.urls')),
    path('api/estadisticas/', include('micsv.svEstadisticas.urls')),
    
    path("dashboard", TemplateView.as_view(template_name="templates/dashboard.html")),
    path("estadisticas/motivo-mes",TemplateView.as_view(template_name="templates/estadisticas/motivo_mes.html")),
    path("estadisticas/alumnos-por-filtros",TemplateView.as_view(template_name="templates/estadisticas/alumnos_por_filtros.html")),
    path("estadisticas/uso-semana/", TemplateView.as_view(template_name="templates/estadisticas/uso_semana.html")),
    
    path("gestion/alumnos", TemplateView.as_view(template_name="templates/gestion/alumnos.html")),
    path("gestion/profesores", TemplateView.as_view(template_name="templates/gestion/profesores.html")),
    path("gestion/asignaturas", TemplateView.as_view(template_name="templates/gestion/asignaturas.html")),
    path("gestion/maquinas", TemplateView.as_view(template_name="templates/gestion/maquinas.html")),
    
    path("acceso/registro/libre",  TemplateView.as_view(template_name="templates/acceso/registro_libre.html")),
    path("acceso/registro/clase", TemplateView.as_view(template_name="templates/acceso/registro_clase.html")),
    path("acceso/registro/salida", TemplateView.as_view(template_name="templates/acceso/registro_base.html")),
    
    # Vista por defecto del index
    path('', TemplateView.as_view(template_name="templates/dashboard.html")),
]
