from django.shortcuts import render
from aparcamientos import parser
from aparcamientos.models import Aparcamiento
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def main(request):

    return render(request, 'aparcamientos/main.html',{})







def load_xml(request):
    aparcamientos = Aparcamiento.objects.all()
    if len(aparcamientos) == 0:
        parser.init_db()    # Cargamos la base de datos si no tiene aún aparcamientos
        respuesta = 'Base de datos cargada'
    else:
        respuesta = 'La base de datos ya estaba cargada'

    return HttpResponse(respuesta)
