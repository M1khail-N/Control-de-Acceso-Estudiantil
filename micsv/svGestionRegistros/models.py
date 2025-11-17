from django.db import models

# Tabla Profesor
class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    class Meta:
        app_label = 'svGestionRegistros'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Tabla Asignatura
class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.PROTECT, related_name='asignaturas')
    nombre = models.CharField(max_length=150)
    
    class Meta:
        app_label = 'svGestionRegistros'

    def __str__(self):
        return self.nombre

# Tabla Maquina
class Maquina(models.Model):
    id_maquina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'svGestionRegistros'

    def __str__(self):
        return self.nombre

# Tabla Alumno
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    codigo_alumno = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    ciclo = models.PositiveSmallIntegerField()
    fecha_nacimiento = models.DateField()
    
    class Meta:
        app_label = 'svGestionRegistros'

    def __str__(self):
        return f"{self.codigo_alumno} - {self.nombre} {self.apellido}"

    class Meta:
        indexes = [models.Index(fields=['codigo_alumno'])]