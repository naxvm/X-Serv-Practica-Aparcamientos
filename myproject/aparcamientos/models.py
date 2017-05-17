from django.db import models

# Create your models here.

class Estilo(models.Model):
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



class Aparcamiento(models.Model):
    # De momento serán todos TextField
   nombre = models.TextField() 

from django.contrib.auth.models import User
class Comentario(models.Model):
    contenido = models.TextField()
    hora = models.DateTimeField()
    aparcamiento = models.ForeignKey(Aparcamiento,null=True, blank=True)  
    selected_by = models.ManyToManyField(User,null=True, blank=True)
