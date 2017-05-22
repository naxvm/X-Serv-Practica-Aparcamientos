from django.shortcuts import render
from aparcamientos import parser
from aparcamientos.models import Aparcamiento
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

distritos = {}

# Create your views here.
def main(request):

    aparcamientos = Aparcamiento.objects.all()
    return render(request, 'aparcamientos/main.html',{'aparcamientos': aparcamientos})



def load_xml(request):
    aparcamientos = Aparcamiento.objects.all()
    vacia = (len(aparcamientos) == 0)
    if vacia:
        distritos = parser.init_db()    # Cargamos la base de datos si no tiene aún aparcamientos

    return render(request, 'aparcamientos/redirect_to_main.html', {})

def aparcamientos(request):
    aparcamientos = Aparcamiento.objects.all()
    for aparcamiento in aparcamientos:
        print(str(aparcamiento.id))

    return render(request, 'aparcamientos/mostrar_aparcamientos.html',{ 'aparcamientos': aparcamientos })

def ver_aparcamiento(request,numero):
    # Delegamos en la plantilla el controlar que el aparcamiento no exista
    mi_aparcamiento = None
    try:
        mi_aparcamiento = Aparcamiento.objects.get(identificador=numero)
        print(mi_aparcamiento.nombre)
    except:
        pass
    return render(request, 'aparcamientos/mi_aparcamiento.html',{ 'aparcamiento': mi_aparcamiento })

@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        my_username = request.POST['username']
        my_password = request.POST['password']

        usuario = authenticate(username=my_username, password=my_password)

        if (not usuario or not usuario.is_active):
            texto = '<font color="red">Login incorrecto. Revisa tus datos</font>'
            redirigir = 0
        else:
            login(request,usuario) # Envía la cookie de sesión, entre otros
            texto = '<font color="green">Login correcto. Te estamos redirigiendo a la página principal...</font>'
            redirigir = 1
    else:   # GET
        texto = 'Introduce tus datos para iniciar sesión'
        redirigir = 0

    return render(request, 'aparcamientos/login.html', {'texto': texto, 'redirigir': redirigir})
