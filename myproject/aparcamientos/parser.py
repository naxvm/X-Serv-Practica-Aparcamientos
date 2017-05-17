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

def cargar_db():

   aparcamientosMadrid = parsear(entries)
   return aparcamientosMadrid
