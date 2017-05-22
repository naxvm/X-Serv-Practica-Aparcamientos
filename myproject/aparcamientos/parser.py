import xmltodict
from urllib import request

url_str = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'
xml_str = request.urlopen(url_str).read()  # Lee el documento como un string
document = xmltodict.parse(xml_str)  # Parsea el documento
entries = document['Contenidos']['contenido']  # Aqui nos quedamos solo con los contenidos (el resto era info del dataset)


def parsear_aparcamiento(lista):
    aparcamiento = {}
    for propiedad in lista:
        if len(propiedad) == 2:
            try:
                aparcamiento[propiedad['@nombre']] = propiedad['#text']
            except KeyError:
                # Para los campos multiples hay que llamar recursivamente a la funcion para parsear
                aparcamiento[propiedad['@nombre']] = parsear_aparcamiento(propiedad['atributo'])

    return aparcamiento


def parsear(nodos):
    total = []
    for aparcamiento in nodos:
        total.append(parsear_aparcamiento(aparcamiento['atributos']['atributo']))
    return total


"""
Ahora vamos a añadir todos los aparcamientos a la base de datos de la aplicación. Tendremos que importarla, y crear el método correspondiente, al que llamaremos desde '/load_xml' en views.py
"""
from .models import Aparcamiento

def init_db():
    # Tenemos que crear además una lista de distritos, para el filtro de distritos.
    distritos = {}
    aparcamientosMadrid = parsear(entries)

    for aparcamiento in aparcamientosMadrid:
        print(aparcamiento['NOMBRE'])
        descripcionAux = None
        distritoAux = None
        barrioAux = None
        try:
            descripcionAux = aparcamiento['DESCRIPCION']
        except KeyError:
            try:    # Para arreglar el aparcamiento que tiene el atributo cambiado
                descripcionAux = aparcamiento['DESCRIPCION-ENTIDAD']
            except KeyError:
                pass
        try:
            distritoAux = aparcamiento['LOCALIZACION']['DISTRITO']
            if not distritoAux in distritos:
                print('NUEVO')
        except KeyError:
            pass

        try:
            barrioAux = aparcamiento['LOCALIZACION']['BARRIO']
        except KeyError:
            pass

        actual = Aparcamiento(identificador = aparcamiento['ID-ENTIDAD'],
                              nombre = aparcamiento['NOMBRE'],
                              url = aparcamiento['CONTENT-URL'],
                              clase_vial = aparcamiento['LOCALIZACION']['CLASE-VIAL'],
                              nombre_via = aparcamiento['LOCALIZACION']['NOMBRE-VIA'],
                              distrito = distritoAux,
                              barrio = barrioAux,
                              accesibilidad = (aparcamiento['ACCESIBILIDAD'] == '1'),
                              descripcion = descripcionAux,
                              )
        actual.save()


    return distritos
