from django.shortcuts import render, redirect 
from .forms import CustomUserCreationForm 
from django.contrib.auth import login 
from django.contrib import messages

# ✅ Importamos tus cosas
from blog.models import Registro, Usuario, Perfil
from django.utils import timezone


def register(request): 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 1. Guardamos usuario Django
            user = form.save()
            
            # ✅ 2. Guardamos Registro (SIN BUSCAR ANTES, lo creamos directo)
            registro = Registro.objects.create(
                email=user.email,
                contrasena=user.password,
                fecha_registro=timezone.now()
            )

            # ✅ 3. Guardamos Usuario
            usuario = Usuario.objects.create(
                nombre=user.username,
                apellido="",
                registro=registro  # <-- Usamos el que acabamos de crear
            )

            # ✅ 4. Guardamos Perfil
            Perfil.objects.create(
                username=user.username,
                descripcion="¡Hola! Soy nuevo en NextStory. 📚",
                usuario=usuario  # <-- Usamos el que acabamos de crear
            )

            # 5. Sesión y redirección
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta ha sido creada.')
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})