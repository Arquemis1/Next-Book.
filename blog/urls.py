from django.urls import path
from .views import welcome_view, home_page, subir_libro

app_name = 'blog'

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home/', home_page, name='home'),
    path('subir-libro/', subir_libro, name='subir_libro'),
]