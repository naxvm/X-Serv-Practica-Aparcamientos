from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Estilo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)

    # Ahora definimos los tamaños de letra que utilizaremos para el CSS

    # Y el campo para elegirlo
    font_size = models.FloatField(default=1.0)
    # Falta el campo para elegir el color de fondo en el CSS
    background_color = models.CharField(max_length=15,default='white')
    # También faltaba este
    page_title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return ('Estilo de ' + str(self.user) + ": {Fuente: " + str(self.font_size) + '} ' + '{Color: ' + str(self.background_color) + '}')


class SeleccionadoPor(models.Model):
    selected_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default=None)
    aparcamiento = models.ForeignKey('Aparcamiento')
    cuando = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (str(self.aparcamiento))





class Aparcamiento(models.Model):
    # Campos principales del XML
    identificador = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=250, null=True)


    clase_vial=  models.CharField(max_length=100, null=True)
    nombre_via = models.CharField(max_length=100, null=True)
    numero = models.CharField(max_length=10, null=True)
    telefono = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=50, null=True)

    distrito = models.CharField(max_length=100, null=True)
    barrio = models.CharField(max_length=100, null=True)
    latitud = models.CharField(max_length=25, null=True)
    longitud = models.CharField(max_length=25, null=True)

    accesibilidad = models.BooleanField(default=False)
    descripcion = models.TextField(null=True)

    # Campo aparte para seleccionar el aparcamiento como favorito"
    numero_comentarios = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    contenido = models.TextField()
    hora = models.DateTimeField()
    aparcamiento = models.ForeignKey(Aparcamiento,null=True, blank=True)

    def __str__(self):
        return self.contenido
