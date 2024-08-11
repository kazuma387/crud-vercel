from django.db import models
from django.contrib.auth.models import User


# creando DB de representantes
class Representante(models.Model):
    cedula = models.CharField(max_length=10, unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=30, blank=False, null=False)
    apellidos = models.CharField(max_length=30, blank=False, null=False)
    serial_patria = models.IntegerField(blank=True, null=True)
    codigo_patria = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    direccion = models.TextField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - C.I: {self.cedula}"

# creando DB de Alumnos
class Alumno(models.Model):
    nombres = models.CharField(max_length=30, blank=False, null=False)
    apellidos = models.CharField(max_length=30, blank=False, null=False)
    edad = models.IntegerField(blank=False, null=False)
    sexo = models.CharField(max_length=9, blank=False, null=False)
    grado_y_seccion = models.CharField(max_length=12, blank=False, null=False)
    fecha_de_nacimiento = models.DateField(blank=False, null=False)
    lugar_de_nacimiento = models.TextField(max_length=255, blank=False, null=False)
    # para asociar cada uno de los alumnos con el representante
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE, related_name='alumno')

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - Grado/sección: {self.grado_y_seccion}"

# creando DB de eliminados
class RegistroEliminado(models.Model):
    tipo = models.CharField(max_length=20)  # 'representante' o 'alumno'
    datos = models.JSONField()
    eliminado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} eliminado el {self.fecha_eliminacion}"