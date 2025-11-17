from django.contrib import admin
from .models import RegistroBase, RegistroLibre, RegistroClase


@admin.register(RegistroBase)
class RegistroBaseAdmin(admin.ModelAdmin):
    list_display = ('id_reg_base','alumno','maquina','fecha_hora_entrada','fecha_hora_salida')


@admin.register(RegistroLibre)
class RegistroLibreAdmin(admin.ModelAdmin):
    list_display = ('reg_base','motivo')


@admin.register(RegistroClase)
class RegistroClaseAdmin(admin.ModelAdmin):
    list_display = ('reg_base','asignatura','profesor')