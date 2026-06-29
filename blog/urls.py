# blog/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    # Página de bienvenida (raíz del sitio)
    path('', views.welcome_view, name='welcome'),

    # Home / catálogo principal
    path('home/', views.home_page, name='home'),

    # Perfil del usuario logueado (sin ID)
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Perfil de otro usuario por ID — mismo nombre, Django elige el que coincide
    path('perfil/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),

    # Perfil de un libro
    path('libro/<int:libro_id>/', views.perfil_libro, name='perfil_libro'),

    # Subir / escribir libro
    path('escribir/', views.subir_libro, name='subir_libro'),

    # Guardar libro (POST desde el editor)
    path('escribir/guardar/', views.guardar_libro, name='guardar_libro'),

    # Panel de administrador
    path('admin-panel/', views.panel_administrador, name='panel_administrador'),

    # Registro de nuevo usuario
    path('registro/', views.registro, name='registro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)