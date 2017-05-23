from django.shortcuts import render
from aparcamientos import parser
from aparcamientos import models
from aparcamientos.models import Aparcamiento, Comentario, SeleccionadoPor, Estilo
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import datetime



def estilo_usuario(usuario):
    mi_usuario = User.objects.get(username=usuario)
    try:
        mi_estilo = Estilo.objects.get(user=mi_usuario)
        fuente = mi_estilo.font_size
        titulo = mi_estilo.page_title
        color_fondo = mi_estilo.background_color
    except Estilo.DoesNotExist:
        fuente = 1.0
        titulo = ("Página de " + str(usuario))
        color_fondo = 'white'

    return (fuente, titulo, color_fondo)


# Create your views here.
def main(request):

    aparcamientos = Aparcamiento.objects.all()
    mas_comentados = Aparcamiento.objects.filter(numero_comentarios__gt = 0)
    mas_comentados = mas_comentados.order_by('-numero_comentarios')[0:5]

    paginas = {}
    # Obtenemos las páginas de usuarios
    for usuario in User.objects.all():
        print('-------- ', usuario)
        try:
            titulo = Estilo.objects.get(user=usuario).page_title
            if not titulo:
                titulo = ('Página de ' + str(usuario))
        except Estilo.DoesNotExist:
            titulo = ('Página de ' + str(usuario))
            print('Not found. ', titulo)
        print(titulo)
        paginas[usuario] = titulo



    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        pagina = render(request, 'aparcamientos/private/main.html',{'usuario': request.user,'estilo': estilo, 'aparcamientos': aparcamientos, 'mas_comentados': mas_comentados, 'paginas': paginas})
    else:
        pagina = render(request, 'aparcamientos/public/main.html',{'aparcamientos': aparcamientos, 'mas_comentados': mas_comentados, 'paginas': paginas})

    return pagina



def load_xml(request):
    aparcamientos = Aparcamiento.objects.all()
    if not aparcamientos:
        distritos = parser.init_db()    # Cargamos la base de datos si no tiene aún aparcamientos

    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        respuesta = render(request, 'aparcamientos/private/redirect_to_main.html',{'usuario': request.user})
    else:
        respuesta = render(request, 'aparcamientos/public/redirect_to_main.html',{})
    return respuesta

def aparcamientos(request):
    distritos = []
    distrito_filtro = None
    aparcamientos = Aparcamiento.objects.all()

    for aparcamiento in aparcamientos:
        if not aparcamiento.distrito in distritos:
            distritos.append(aparcamiento.distrito)
    try:
        distritos.remove(None)
    except ValueError:
        pass

    if request.method == 'POST':
        distrito_filtro = request.POST['distrito']
        if distrito_filtro != 'todos':
            aparcamientos = aparcamientos.filter(distrito=distrito_filtro)


    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        respuesta = render(request, 'aparcamientos/private/mostrar_aparcamientos.html',{'usuario': request.user,'estilo': estilo, 'aparcamientos': aparcamientos, 'accesibles': 0, 'distritos': distritos, 'distrito_filtro': distrito_filtro})
    else:
        respuesta = render(request, 'aparcamientos/public/mostrar_aparcamientos.html',{'aparcamientos': aparcamientos, 'accesibles': 0, 'distritos': distritos, 'distrito_filtro': distrito_filtro})

    return respuesta

def ver_aparcamiento(request,numero):
    # Delegamos en la plantilla el controlar que el aparcamiento no exista
    mi_aparcamiento = None
    mis_comentarios = None
    try:
        mi_aparcamiento = Aparcamiento.objects.get(identificador=numero)
    except:
        pass
    if request.method == 'POST': # Hacemos un POST: añadimos un comentario
        comentario = request.POST['comentario']
        objeto_comentario = Comentario(contenido = comentario,
                                       hora = datetime.datetime.now(),
                                       aparcamiento = mi_aparcamiento,
        )
        objeto_comentario.save()

        mi_aparcamiento.numero_comentarios = mi_aparcamiento.numero_comentarios + 1
        mi_aparcamiento.save()

    try:
        mis_comentarios = Comentario.objects.filter(aparcamiento=mi_aparcamiento)
    except:
        pass
    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        usuario = User.objects.get(username=request.user)
        aparcamiento = Aparcamiento.objects.get(identificador=numero)
        seleccionado = SeleccionadoPor.objects.filter(selected_by=usuario,aparcamiento=aparcamiento).count()


        respuesta = render(request, 'aparcamientos/private/mi_aparcamiento.html',{'usuario': usuario,'estilo': estilo, 'aparcamiento': mi_aparcamiento, 'comentarios': mis_comentarios, 'seleccionado': seleccionado})
    else:
        respuesta = render(request, 'aparcamientos/public/mi_aparcamiento.html',{'aparcamiento': mi_aparcamiento, 'comentarios': mis_comentarios, 'seleccionado': seleccionado})

    return respuesta


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

    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        respuesta = render(request, 'aparcamientos/private/login.html',{'usuario': request.user,'estilo': estilo, 'texto': texto, 'redirigir': redirigir})
    else:
        respuesta = render(request, 'aparcamientos/public/login.html',{'texto': texto, 'redirigir': redirigir})
    return respuesta


@csrf_exempt
def logout_page(request):
    logout(request)
    return render(request, 'aparcamientos/private/redirect_to_main.html',{})


def solo_accesibles(request):
    distritos = []
    distrito_filtro = None

    aparcamientos = Aparcamiento.objects.filter(accesibilidad=1)
    for aparcamiento in aparcamientos:
        print(str(aparcamiento.id))
        if not aparcamiento.distrito in distritos:
            distritos.append(aparcamiento.distrito)


    if request.method == 'POST':
        distrito_filtro = request.POST['distrito']
        if distrito_filtro != 'todos':
            aparcamientos = aparcamientos.filter(distrito=distrito_filtro)

    for aparcamiento in aparcamientos:
        print(str(aparcamiento.id))
    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        respuesta = render(request, 'aparcamientos/private/mostrar_aparcamientos.html',{'usuario': request.user,'estilo': estilo, 'aparcamientos': aparcamientos, 'accesibles': 1, 'distritos': distritos, 'distrito_filtro': distrito_filtro})
    else:
        respuesta = render(request, 'aparcamientos/public/mostrar_aparcamientos.html',{'aparcamientos': aparcamientos, 'accesibles': 1, 'distritos': distritos, 'distrito_filtro': distrito_filtro})

    return respuesta


def seleccionar_aparcamiento(request, id):
    usuario = User.objects.get(username=request.user)
    mi_aparcamiento = Aparcamiento.objects.get(identificador=id)
    seleccionado = SeleccionadoPor.objects.create(aparcamiento = mi_aparcamiento)
    seleccionado.selected_by.add(usuario)

    return ver_aparcamiento(request,id)

def deseleccionar_aparcamiento(request, id):
    usuario = User.objects.get(username=request.user)

    aparcamiento = Aparcamiento.objects.get(identificador=id)
    SeleccionadoPor.objects.get(selected_by=usuario, aparcamiento=aparcamiento).delete()
    print('borrado')
    return ver_aparcamiento(request,id)


def user_page(request, username):
    usuario = User.objects.get(username=username)

    if request.method == 'POST':
        nuevo_color = request.POST['bg_color_choose']
        tamano_fuente = request.POST['font_size_choose']
        nuevo_titulo = request.POST['titulo_nuevo']
        print(nuevo_titulo)
        try:
            estilo_de_usuario = Estilo.objects.get(user=usuario)
            print('lo he conseguido: ' + str(estilo_de_usuario))
            estilo_de_usuario.font_size = tamano_fuente
            estilo_de_usuario.background_color = nuevo_color
        except Estilo.DoesNotExist:
            print('no existia')
            estilo_de_usuario = Estilo(user = usuario,
                                       font_size = tamano_fuente,
                                       background_color = nuevo_color)
        if nuevo_titulo:
            estilo_de_usuario.page_title = nuevo_titulo
        print('Voy a guardar esto: ' + str(estilo_de_usuario))
        estilo_de_usuario.save()


    aparcamientos_seleccionados = SeleccionadoPor.objects.filter(selected_by=usuario)
    offset = 0
    backward = True
    forward = True
    try:
        offset = int(request.GET['offset'])
    except KeyError:
        pass

    if offset == 0:
        backward = False

    if 5 * (offset + 1) >= len(aparcamientos_seleccionados):
        forward = False
    seleccionados_trozo = SeleccionadoPor.objects.filter(selected_by=usuario)[offset*5:(offset+1)*5]


    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        print(estilo)
        personalizar = str(username) == str(request.user)
        respuesta = render(request, 'aparcamientos/private/pagina_de.html', {'usuario': usuario,'estilo': estilo, 'offset': offset,'seleccionados': seleccionados_trozo, 'backward': backward, 'forward': forward, 'personalizar': personalizar})
    else:
        respuesta = render(request, 'aparcamientos/public/pagina_de.html', {'usuario': usuario, 'offset': offset, 'seleccionados': seleccionados_trozo, 'backward': backward, 'forward': forward})

    return respuesta




def about(request):
    print(request.user)
    usuario = User.objects.get(username=request.user)

    if request.user.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        respuesta = render(request,'aparcamientos/private/ayuda.html', {'usuario': usuario})
    else:
        respuesta = render(request, 'aparcamientos/public/ayuda.html',{})


    return respuesta
