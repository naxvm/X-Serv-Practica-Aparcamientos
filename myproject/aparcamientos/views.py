from django.shortcuts import render
from aparcamientos import parser
from aparcamientos.models import Aparcamiento
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def main(request):

    return render(request, 'aparcamientos/main.html',{})


def load_xml(request):
    aparcamientos = parser.cargar_db()
    for aparcamiento in aparcamientos:
        print(aparcamiento['NOMBRE'])

        descripcionAux = None
        distritoAux = None
        barrioAux = None
        try:     
            descripcionAux = aparcamiento['DESCRIPCION']
        except KeyError:
            try:   # Para arreglar el aparcamiento que tiene el atributo cambiado
                descripcionAux = aparcamiento['DESCRIPCION-ENTIDAD']
            except KeyError:
                pass

        try:
            distritoAux = aparcamiento['DISTRITO']
        except KeyError:
            pass 

        try:
            barrioAux = aparcamiento['BARRIO']
        except KeyError:
            pass



        actual = Aparcamiento(nombre = aparcamiento['NOMBRE'],
                              clase_vial = aparcamiento['LOCALIZACION']['CLASE-VIAL'],
                              nombre_via = aparcamiento['LOCALIZACION']['NOMBRE-VIA'],
                              distrito = distritoAux,
                              barrio = barrioAux,
                              accesibilidad = (aparcamiento['ACCESIBILIDAD'] == '1'),
                              descripcion = descripcionAux,
                              )
        actual.save()

    return HttpResponse('nikelao')
