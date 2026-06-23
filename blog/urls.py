from django.urls import path
from .views import (
    welcome_view,
    home_page,
    subir_libro,       # ✅ CORRECTO: Así se llama en tu views.py
    guardar_libro,
    perfil_libro,
    perfil_usuario,
    panel_administrador,
    registro
)

# Nombre de la aplicación para usar 'blog:nombre_ruta' en las plantillas
app_name = 'blog'

urlpatterns = [
    # Páginas principales
    path('', welcome_view, name='welcome'),
    path('inicio/', home_page, name='home'),
    
    # Libros
    path('subir-libro/', subir_libro, name='subir_libro'),  # ✅ Ruta corregida
    path('guardar-libro/', guardar_libro, name='guardar_libro'),
    path('libro/<int:libro_id>/', perfil_libro, name='perfil_libro'),

    # Perfiles
    path('perfil/', perfil_usuario, name='mi_perfil'),
    path('perfil/<int:usuario_id>/', perfil_usuario, name='perfil_usuario'),

    # Administración
    path('admin-panel/', panel_administrador, name='panel_admin'),

    # Autenticación / Registro
    path('registro/', registro, name='registro'),
]