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
    # 🏠 Rutas principales
    path('', welcome_view, name='welcome'),          # Página de bienvenida
    path('home/', home_page, name='home'),           # ✅ Coincide con el enlace de invitado
    path('subir-libro/', subir_libro, name='subir_libro'), # ✅ Coincide con el botón del navbar

    # 📚 Rutas de Libros
    path('libro/<int:libro_id>/', perfil_libro, name='perfil_libro'), # ✅ Coincide con tarjetas de libros

    # 👤 Rutas de Perfiles de Usuario
    path('usuario/', perfil_usuario, name='mi_perfil'),                # Mi perfil (el propio usuario)
    path('usuario/<int:usuario_id>/', perfil_usuario, name='perfil_usuario'), # Ver perfil de OTRO usuario

    # ⚙️ Ruta de Administrador
    path('administrador/', panel_administrador, name='panel_admin'), # ✅ Coincide con el menú de admin
]