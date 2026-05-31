from django.shortcuts import render, redirect 
from .forms import CustomUserCreationForm 
from django.contrib.auth import login 
from django.contrib import messages 

def register(request): 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta ha sido creada y has iniciado sesión.')
            # 🔽 CAMBIO: Ahora redirige a tu página principal /inicio/
            return redirect('blog:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})