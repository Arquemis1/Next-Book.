from django.shortcuts import render, redirect
from django.utils import timezone
from .models_generados import Libro
from .forms import LibroForm

# Vista 1: Página de Bienvenida
def welcome_view(request):
    return render(request, 'blog/welcome_page.html')

# Vista 2: Página Principal / Home
def home_page(request):
    lista_libros = Libro.objects.filter(estado='Publicado').order_by('-fecha_creacion')
    return render(request, 'blog/home_page.html', {'libros': lista_libros})

# Vista 3: Subir Libro (⚠️ ESTA ES LA QUE FALTABA LLAMAR)
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