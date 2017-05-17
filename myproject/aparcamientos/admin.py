from django.contrib import admin

# Register your models here.
from .models import Estilo, Aparcamiento, Comentario 


# Hay que registrar los modelos, para que sean visibles desde /admin/
admin.site.register(Estilo)
admin.site.register(Aparcamiento)
admin.site.register(Comentario)
