from django.urls import path
from .views import (
    welcome_view, 
    home_page, 
    subir_libro,
    perfil_libro,
    perfil_usuario,
    panel_administrador
)

app_name = 'blog'

urlpatterns = [
    # Rutas originales
    path('', welcome_view, name='welcome'),
    path('home/', home_page, name='home'),
    path('subir-libro/', subir_libro, name='subir_libro'),

    # ✅ Nuevas rutas agregadas
    path('libro/<int:libro_id>/', perfil_libro, name='perfil_libro'),
    path('usuario/', perfil_usuario, name='mi_perfil'),
    path('usuario/<int:usuario_id>/', perfil_usuario, name='ver_perfil'),
    path('administrador/', panel_administrador, name='panel_admin'),
]