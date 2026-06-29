# ==============================================
# ✅ IMPORTACIONES CORRECTAS
# ==============================================
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
# ✅ Importamos EXACTAMENTE los modelos que existen en models.py
from .models import Usuario, Libro, Administradores, AutorLibro, Perfil, Registro, Reporte, Comentario
from django.db.models import Count
from datetime import datetime
from django.contrib.auth import login  
from django.contrib.auth.models import User  # ✅ Importación necesaria

# ==============================================
# ✅ VISTAS 
# ==============================================

# ------------------------------
# Vista 0: Bienvenida
# ------------------------------
def welcome_view(request):
    return render(request, 'blog/welcome_page.html')


# ------------------------------
# Vista 1: Página Principal / Home
# ------------------------------
def home_page(request):
    libros = Libro.objects.all().order_by('-fecha_creacion')[:20]
    total_libros = Libro.objects.count()
    total_usuarios = Usuario.objects.count()

    usuario_real = None
    perfil_real = None
    es_administrador = False

    if request.user.is_authenticated:
        try:
            # 1. Buscar Registro por email del usuario logueado
            registro = Registro.objects.get(email=request.user.email)
            # 2. Buscar Usuario vinculado a ese registro
            usuario_real = Usuario.objects.get(registro=registro)
            # 3. Buscar Perfil
            perfil_real = Perfil.objects.get(usuario=usuario_real)
            # 4. Verificar si es admin
            es_administrador = Administradores.objects.filter(usuario=usuario_real).exists()
        except (Registro.DoesNotExist, Usuario.DoesNotExist, Perfil.DoesNotExist):
            # Si no existe, dejamos vacío, NO redirigimos
            pass

    contexto = {
        'libros': libros,
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'usuario_real': usuario_real,
        'perfil_real': perfil_real,
        'es_administrador': es_administrador,
    }
    return render(request, 'blog/home_page.html', contexto)


# ------------------------------
# ✅ VISTA 2: SUBIR LIBRO (AHORA ES EL EDITOR NUEVO)
# ------------------------------
@login_required
def subir_libro(request):
    # Simplemente carga la plantilla del editor que creamos
    return render(request, 'blog/escribir_libro.html')


# ------------------------------
# ✅ NUEVA VISTA: GUARDAR LIBRO EN LA BASE DE DATOS (ACTUALIZADA CON PORTADA)
# ------------------------------
@login_required
def guardar_libro(request):
    if request.method == 'POST':
        # 1. Recibir los datos enviados desde el formulario
        titulo = request.POST.get('titulo', 'Sin título').strip()
        sinopsis = request.POST.get('sinopsis', '').strip()
        contenido = request.POST.get('contenido', '')

        # ✅ NUEVO: Recibir la imagen de portada si se envió
        portada = request.FILES.get('portada')

        # Validación básica
        if not titulo:
            return redirect('blog:subir_libro')

        # 2. Obtener al usuario actual con tu lógica exacta
        try:
            registro = Registro.objects.get(email=request.user.email)
            usuario_actual = Usuario.objects.get(registro=registro)
        except (Registro.DoesNotExist, Usuario.DoesNotExist):
            return redirect('blog:welcome')

        # 3. CREAR EL NUEVO LIBRO
        nuevo_libro = Libro.objects.create(
            titulo=titulo,
            sinopsis=sinopsis,
            fecha_creacion=timezone.now(),
            estado='publicado',
            archivo_pdf=contenido,
            # ✅ NUEVO: Asignar la imagen si existe
            portada=portada
        )

        # 4. CREAR LA RELACIÓN AUTOR <-> LIBRO
        AutorLibro.objects.create(
            usuario=usuario_actual,
            libro=nuevo_libro,
            rol='Autor'
        )

        # 5. Redirigir al perfil del libro para verlo completo
        return redirect('blog:perfil_libro', libro_id=nuevo_libro.id_libro)

    return redirect('blog:subir_libro')


# ------------------------------
# Vista 4: Perfil del Libro
# ------------------------------
def perfil_libro(request, libro_id):
    # ✅ Usamos id_libro tal cual está definido en tu modelo
    libro = get_object_or_404(Libro, id_libro=libro_id)
    autor_link = AutorLibro.objects.filter(libro=libro).first()
    autor = autor_link.usuario if autor_link else None

    contexto = {
        'libro': libro,
        'autor': autor,
        'valoracion_promedio': 4.8,
        'cantidad_votos': 124,
        'cantidad_paginas': 250,
    }
    return render(request, 'blog/perfil_libro.html', contexto)


# ------------------------------
# ✅ VISTA PERFIL DE USUARIO ARREGLADA ✅
# ------------------------------
@login_required
def perfil_usuario(request, usuario_id=None):
    usuario = None
    perfil = None

    # CASO 1: Es MI PERFIL (no me pasan ID)
    if not usuario_id:
        try:
            # Buscar mis datos correctamente
            registro = Registro.objects.get(email=request.user.email)
            usuario = Usuario.objects.get(registro=registro)
            usuario_id = usuario.id
        except (Registro.DoesNotExist, Usuario.DoesNotExist):
            return render(request, 'blog/perfil_usuario.html', {
                'error': 'No se encontró tu registro de usuario. ¿Estás registrado correctamente?'
            })
    # CASO 2: Es el perfil de OTRO usuario
    else:
        usuario = get_object_or_404(Usuario, id=usuario_id)

    # Obtener perfil y libros
    try:
        perfil = Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        perfil = None

    # Obtener libros del usuario
    ids_libros = AutorLibro.objects.filter(usuario=usuario).values_list('libro_id', flat=True)
    mis_libros = Libro.objects.filter(id_libro__in=ids_libros).order_by('-fecha_creacion')

    contexto = {
        'usuario': usuario,
        'perfil': perfil,
        'mis_libros': mis_libros,
        'total_libros': mis_libros.count(),
        'seguidores': 150,
        'siguiendo': 85,
        'total_paginas': 3200,
        'libros_favoritos': [],
    }
    return render(request, 'blog/perfil_usuario.html', contexto)


# ------------------------------
# Vista 6: Panel de Administrador
# ------------------------------
def es_administrador(usuario):
    try:
        registro = Registro.objects.get(email=usuario.email)
        usuario_real = Usuario.objects.get(registro=registro)
        return Administradores.objects.filter(usuario=usuario_real).exists()
    except:
        return False

@login_required
@user_passes_test(es_administrador)
def panel_administrador(request):
    todos_usuarios = Usuario.objects.all().order_by('-id')
    todos_libros = Libro.objects.all().order_by('-fecha_creacion')
    todos_admins = Administradores.objects.all()
    reportes_activos = Reporte.objects.count()
    comentarios_pendientes = Comentario.objects.count()

    contexto = {
        'total_usuarios': todos_usuarios.count(),
        'total_libros': todos_libros.count(),
        'fecha_actual': timezone.now(),
        'crecimiento_usuarios': 12.5,
        'crecimiento_libros': 8.2,
        'comentarios_pendientes': comentarios_pendientes,
        'reportes_activos': reportes_activos,
        'ultimos_usuarios': todos_usuarios[:5],
        'lista_usuarios': todos_usuarios,
        'lista_libros': todos_libros,
        'lista_administradores': todos_admins,
        'lista_categorias': [],
        'lista_reportes': Reporte.objects.all(),
        'usuario_actual': request.user
    }
    return render(request, 'blog/panel_admin.html', contexto)


# ==============================================
# ✅ VISTA DE REGISTRO
# ==============================================
def registro(request):
    if request.method == 'POST':
        # Recibir datos que vienen del formulario HTML
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        telefono = request.POST.get('telefono', '')

        try:
            # 1. CREAR USUARIO EN DJANGO (Sistema de login)
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=password
            )
            user.save()

            # 2. GUARDAR EN TU TABLA "REGISTRO"
            registro_nuevo = Registro.objects.create(
                email=email,
                contrasena=password,
                telefono=telefono,
                fecha_registro=timezone.now()
            )

            # 3. GUARDAR EN TU TABLA "USUARIO"
            usuario_nuevo = Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                registro=registro_nuevo
            )

            # 4. CREAR SU PERFIL
            Perfil.objects.create(
                username=user.username,
                descripcion="¡Hola! Soy nuevo en NextStory. 📚",
                usuario=usuario_nuevo
            )

            # 5. INICIAR SESIÓN AUTOMÁTICAMENTE
            login(request, user)

            # 6. REDIRIGIR AL INICIO
            return redirect('blog:home')

        except Exception as e:
            return render(request, 'blog/registro.html', {
                'error': 'Este correo ya está registrado o hubo un error.'
            })

    return render(request, 'blog/registro.html')

    