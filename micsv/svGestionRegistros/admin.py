from django.contrib import admin
from .models import Profesor, Asignatura, Maquina, Alumno


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('id_profesor','nombre','apellido')


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('id_asignatura','nombre','profesor')


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('id_maquina','nombre')


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('id_alumno','codigo_alumno','nombre','apellido','carrera','ciclo')
    search_fields = ('codigo_alumno','nombre','apellido')