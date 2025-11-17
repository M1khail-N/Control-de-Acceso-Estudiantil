from django.db import models
from micsv.svGestionRegistros.models import Alumno, Maquina, Asignatura, Profesor

# Tabla RegistroBase (Padre)
class RegistroBase(models.Model):
    id_reg_base = models.AutoField(primary_key=True)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT)
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        app_label = 'svRegAcceso'

    def __str__(self):
        return f"Registro {self.id_reg_base} - {self.alumno} - {self.maquina}"

# Tabla RegistroLibre (Hijo)
class RegistroLibre(models.Model):
    reg_base = models.OneToOneField(RegistroBase, on_delete=models.CASCADE, primary_key=True, related_name='libre')
    MOTIVO_CHOICES = [
        ('correo','Revisar correo'),
        ('proyecto','Proyecto'),
        ('trabajo','Trabajo'),
        ('extra','Extra clase'),
        ('otro','Otro'),
    ]
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    
    class Meta:
        app_label = 'svRegAcceso'

    def __str__(self):
        return f"Libre {self.reg_base_id} - {self.motivo}"

# Tabla RegistroClase (Hijo)
class RegistroClase(models.Model):
    reg_base = models.OneToOneField(RegistroBase, on_delete=models.CASCADE, primary_key=True, related_name='clase')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.PROTECT)
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT)
    
    class Meta:
        app_label = 'svRegAcceso'

    def __str__(self):
        return f"Clase {self.reg_base_id} - {self.asignatura}"