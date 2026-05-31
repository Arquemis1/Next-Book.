from django import forms
from .models_generados import Libro  # Usamos su tabla

class LibroForm(forms.ModelForm):
    # Agregamos un campo extra para subir el archivo (porque en su tabla es solo texto/ruta)
    archivo_pdf_subir = forms.FileField(label="Seleccionar Archivo PDF")

    class Meta:
        model = Libro
        # ✅ Solo los campos que EXISTEN en la tabla de ustedes
        fields = ['titulo', 'sinopsis', 'estado']

        labels = {
            'titulo': 'Título del Libro',
            'sinopsis': 'Sinopsis / Resumen',
            'estado': 'Estado (ej: Publicado, Borrador)',
        }