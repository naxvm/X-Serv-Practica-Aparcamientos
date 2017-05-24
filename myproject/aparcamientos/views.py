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
        color_fondo = "rgb(34, 34, 34)"

    return (fuente, titulo, color_fondo)

def main(request):
    aparcamientos = Aparcamiento.objects.all()
    mas_comentados = Aparcamiento.objects.filter(numero_comentarios__gt = 0)
    mas_comentados = mas_comentados.order_by('-numero_comentarios')[0:5]

    paginas = {}
    # Obtenemos las páginas de usuarios
    for usuario in User.objects.all():
        try:
            titulo = Estilo.objects.get(user=usuario).page_title
            if not titulo:
                titulo = ('Página de ' + str(usuario))
        except Estilo.DoesNotExist:
            titulo = ('Página de ' + str(usuario))
        paginas[str(usuario)] = titulo

    usuario = request.user
    estilo = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}

    contexto = {'inicio': True,
                'usuario': usuario,
                'estilo': estilo,
                'aparcamientos': aparcamientos,
                'mas_comentados': mas_comentados,
                'paginas': paginas}
    return render(request, 'aparcamientos/main.html',contexto)


def load_xml(request):
    aparcamientos = Aparcamiento.objects.all()
    if not aparcamientos:
        distritos = parser.init_db()    # Cargamos la base de datos si no tiene aún aparcamientos
    usuario = request.user
    estilo = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
    contexto = {'estilo': estilo,'usuario': usuario}
    return render(request, 'aparcamientos/redirect_to_main.html',contexto)


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

    estilo = None
    usuario = request.user
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(request.user)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
    contexto = {'usuario': usuario,
                'estilo': estilo,
                'aparcamientos': aparcamientos,
                'accesibles': 0,
                'distritos': distritos,
                'distrito_filtro': distrito_filtro}
    return render(request, 'aparcamientos/mostrar_aparcamientos.html',contexto)


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

    usuario = request.user
    estilo = None
    seleccionado = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        aparcamiento = None
        try:
            aparcamiento = Aparcamiento.objects.get(identificador=numero)
        except Aparcamiento.DoesNotExist:
            pass
        seleccionado = SeleccionadoPor.objects.filter(selected_by=usuario,aparcamiento=aparcamiento).exists()


    contexto = {'usuario': usuario,
                'estilo': estilo,
                'aparcamiento': mi_aparcamiento,
                'comentarios': mis_comentarios,
                'seleccionado': seleccionado}
    return render(request, 'aparcamientos/mi_aparcamiento.html',contexto)


def login_page(request):
    if request.method == 'POST':
        my_username = request.POST['username']
        my_password = request.POST['password']
        usuario = authenticate(username=my_username, password=my_password)
        if (not usuario or not usuario.is_active):
            if request.POST['action'] == 'login':
                texto = '<font color="red">Login incorrecto. Revisa tus datos</font>'
                redirigir = 0
            else:
                user = User.objects.create_user(username=my_username,
                                                password=my_password)
                login(request,user)
                texto = '<font color="green">¡Bienvenido ' + str(user) + '! Te estamos redirigiendo a la página principal...</font>'
                redirigir = 1
        else:
            if request.POST['action'] == 'login':
                login(request,usuario) # Envía la cookie de sesión, entre otros
                texto = '<font color="green">Login correcto. Te estamos redirigiendo a la página principal...</font>'
                redirigir = 1
            else:
                texto = '<font color="red">Este usuario ya existe. Elige otro nombre de usuario</font>'
                redirigir = 0
    else:   # GET
        texto = 'Introduce tus datos para iniciar sesión'
        redirigir = 0

    usuario = request.user
    estilo = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
    contexto = {'usuario': usuario,
                'estilo': estilo,
                'texto': texto,
                'redirigir': redirigir}
    return render(request, 'aparcamientos/login.html', contexto)


def logout_page(request):
    logout(request)
    return render(request, 'aparcamientos/redirect_to_main.html',{})


def solo_accesibles(request):
    distritos = []
    distrito_filtro = None

    aparcamientos = Aparcamiento.objects.filter(accesibilidad=1)
    for aparcamiento in aparcamientos:
        if not aparcamiento.distrito in distritos:
            distritos.append(aparcamiento.distrito)


    if request.method == 'POST':
        distrito_filtro = request.POST['distrito']
        if distrito_filtro != 'todos':
            aparcamientos = aparcamientos.filter(distrito=distrito_filtro)

    for aparcamiento in aparcamientos:
        if not aparcamiento.distrito in distritos:
            distritos.append(aparcamiento.distrito)
    usuario = request.user
    estilo = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
    contexto = {'usuario': usuario,
                'estilo': estilo,
                'aparcamientos': aparcamientos,
                'accesibles': 1,
                'distritos': distritos,
                'distrito_filtro': distrito_filtro}
    return render(request, 'aparcamientos/mostrar_aparcamientos.html', contexto)


def seleccionar_aparcamiento(request, id):
    usuario = User.objects.get(username=request.user)
    mi_aparcamiento = Aparcamiento.objects.get(identificador=id)
    seleccionado = SeleccionadoPor.objects.create(aparcamiento = mi_aparcamiento)
    seleccionado.selected_by.add(usuario)
    print(request.path)

    return ver_aparcamiento(request,id)

def deseleccionar_aparcamiento(request, id):
    usuario = User.objects.get(username=request.user)
    aparcamiento = Aparcamiento.objects.get(identificador=id)
    SeleccionadoPor.objects.filter(selected_by=usuario, aparcamiento=aparcamiento).delete()
    return ver_aparcamiento(request,id)


def user_page(request, username):
    try:
        usuario_de_pagina = User.objects.get(username=username)
    except User.DoesNotExist:
        return not_found(request,username)
    usuario = request.user

    if request.method == 'POST':
        nuevo_color = request.POST['bg_color_choose']
        tamano_fuente = request.POST['font_size_choose']
        nuevo_titulo = request.POST['titulo_nuevo']
        try:
            estilo_de_usuario = Estilo.objects.get(user=usuario)
            estilo_de_usuario.font_size = tamano_fuente
            estilo_de_usuario.background_color = nuevo_color
        except Estilo.DoesNotExist:
            estilo_de_usuario = Estilo(user = usuario_de_pagina,
                                       font_size = tamano_fuente,
                                       background_color = nuevo_color)
        if nuevo_titulo:
            estilo_de_usuario.page_title = nuevo_titulo
        estilo_de_usuario.save()


    aparcamientos_seleccionados = SeleccionadoPor.objects.filter(selected_by=usuario_de_pagina)
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
    seleccionados_trozo = SeleccionadoPor.objects.filter(selected_by=usuario_de_pagina)[offset*5:(offset+1)*5]

    usuario = request.user
    estilo = None
    personalizar = None
    if usuario.is_authenticated:
        (fuente, _, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
        personalizar = str(username) == str(usuario)
    (_, titulo_de_pagina, _ ) = estilo_usuario(usuario_de_pagina)
    contexto = {'usuario': usuario,
                'usuario_de_pagina': usuario_de_pagina,
                'titulo_de_pagina': titulo_de_pagina,
                'estilo': estilo,
                'offset': offset,
                'seleccionados': seleccionados_trozo,
                'backward': backward,
                'forward': forward,
                'personalizar': personalizar}
    return render(request,'aparcamientos/pagina_de.html', contexto)



def about(request):
    try:
        usuario = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    usuario = request.user
    estilo = None
    if usuario.is_authenticated:
        (fuente, titulo, color_fondo) = estilo_usuario(usuario)
        estilo = {'fuente': fuente, 'color_fondo': color_fondo}
    contexto = {'usuario': usuario,
                'estilo': estilo}
    return render(request,'aparcamientos/ayuda.html', contexto)


def user_xml(request, user):
    usuario = User.objects.get(username=user)
    aparcamientos_seleccionados = []
    nombres_seleccionados = SeleccionadoPor.objects.filter(selected_by=usuario)
    for nombre in nombres_seleccionados:
        aparcamientos_seleccionados.append(Aparcamiento.objects.get(nombre=nombre))
    contexto = {'usuario': usuario,
                'aparcamientos_seleccionados': aparcamientos_seleccionados}
    return render(request, 'aparcamientos/user_xml.html', contexto, content_type="text/xml")

def not_found(request,resource):

    contexto = {'recurso': resource}

    return render(request, 'aparcamientos/not_found.html', contexto)
