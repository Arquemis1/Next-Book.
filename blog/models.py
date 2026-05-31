from django.db import models
from django.utils import timezone # Importamos timezone para la fecha

class Post(models.Model):
    title = models.CharField(max_length=200) # Un campo de texto corto para el título
    content = models.TextField() # Un campo de texto largo para el contenido
    published_date = models.DateTimeField(default=timezone.now) # Fecha de publicación automática

    def __str__(self):
        return self.title # Muestra el título del post en el panel de administración
# Create your models here.
