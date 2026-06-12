from django.shortcuts import render, redirect, get_object_or_404  # ✅ Agregado get_object
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test  # ✅ Agregados para seguridad
from .models_generados import Libro, Usuario, Administradores  # ✅ Agregados los modelos Usuario y Admin
from .forms import LibroForm

# ------------------------------
# Vista 1: Página de Bienvenida
# ------------------------------
def welcome_view(request):
    return render(request, 'blog/welcome_page.html')

# ------------------------------
# Vista 2: Página Principal / Home
# ------------------------------
def home_page(request):
    lista_libros = Libro.objects.filter(estado='Publicado').order_by('-fecha_creacion')
    return render(request, 'blog/home_page.html', {'libros': lista_libros})

# ------------------------------
# Vista 3: Subir Libro
# ------------------------------
def subir_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_pdf = request.FILES['archivo_pdf_subir']
            ruta_guardado = f"libros/{archivo_pdf.name}"

            nuevo_libro = Libro(
                titulo = form.cleaned_data['titulo'],
                sinopsis = form.cleaned_data['sinopsis'],
                estado = form.cleaned_data['estado'],
                fecha_creacion = timezone.now(),
                archivo_pdf = ruta_guardado
            )
            nuevo_libro.save()
            return redirect('blog:home')
    else:
        form = LibroForm()
    return render(request, 'blog/subir_libro.html', {'form': form})


# ==============================================
# ✅ NUEVAS VISTAS AGREGADAS (PERFIL Y ADMIN)
# ==============================================

# ------------------------------
# Vista 4: Perfil del Libro
# ------------------------------
def perfil_libro(request, libro_id):
    # Busca el libro específico, si no existe da error 404
    libro = get_object_or_404(Libro, id_libro=libro_id)
    return render(request, 'blog/perfil_libro.html', {'libro': libro})


# ------------------------------
# Vista 5: Perfil de Usuario
# ------------------------------
@login_required  # 🔒 Solo entra si ha iniciado sesión
def perfil_usuario(request, usuario_id=None):
    # Si no se especifica ID, carga el perfil del usuario actual
    if not usuario_id:
        usuario_id = request.user.id_usuario  # ⚠️ Ajusta 'id_usuario' al nombre exacto de tu campo PK

    usuario = get_object_or_404(Usuario, id_usuario=usuario_id) # ⚠️ Ajusta el nombre del campo si es distinto
    # Obtener los libros que ha subido o guardado este usuario
    mis_libros = Libro.objects.filter(usuario_id=usuario_id).order_by('-fecha_creacion') # ⚠️ Ajusta la relación

    return render(request, 'blog/perfil_usuario.html', {
        'usuario': usuario,
        'mis_libros': mis_libros
    })


# ------------------------------
# Vista 6: Panel de Administrador
# ------------------------------
# Función para verificar si es administrador
def es_administrador(usuario):
    # Verifica si el usuario está en la tabla de Administradores
    return Administradores.objects.filter(id_usuario=usuario.id_usuario).exists() # ⚠️ Ajusta campos si es necesario

@login_required  # 🔒 Requiere sesión
@user_passes_test(es_administrador)  # 🔒 SOLO si es admin
def panel_administrador(request):
    # Cargar todos los datos para las tablas
    todos_usuarios = Usuario.objects.all()
    todos_libros = Libro.objects.all()
    todos_admins = Administradores.objects.all()

    return render(request, 'blog/panel_admin.html', {
        'usuarios': todos_usuarios,
        'libros': todos_libros,
        'administradores': todos_admins
    })