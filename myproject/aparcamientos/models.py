from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Estilo(models.Model):
    user = models.OneToOneField(User, null=True)
    # Ahora definimos los tamaños de letra que utilizaremos para el CSS

    SIZE_CHOICES = (
        (5.0, 'HUGE'),
        (3.0, 'LARGE'),
        (1.0, 'NORMAL'),
        (0.75,'SMALL'),
        (0.5, 'TINY'),
    )
    # Y el campo para elegirlo
    font_size = models.FloatField(choices=SIZE_CHOICES, default=1.0)
    # Falta el campo para elegir el color de fondo en el CSS

    # También faltaba este
    page_title = models.CharField(max_length=100, null=True)

class Aparcamiento(models.Model):
    # Campos principales del XML
    identificador = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=250, null=True)


    clase_vial=  models.CharField(max_length=100, null=True)
    nombre_via = models.CharField(max_length=100, null=True)

    distrito = models.CharField(max_length=100, null=True)
    barrio = models.CharField(max_length=100, null=True)

    accesibilidad = models.BooleanField(default=False)
    descripcion = models.TextField(null=True)

    # Campo aparte para seleccionar el aparcamiento como favorito"
    selected_by = models.ManyToManyField(User, blank=True, default=None)
    numero_comentarios = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    contenido = models.TextField()
    hora = models.DateTimeField()
    aparcamiento = models.ForeignKey(Aparcamiento,null=True, blank=True)

    def __str__(self):
        return self.contenido
