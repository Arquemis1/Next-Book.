from django.db import models
from django.utils import timezone


class Registro(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    contrasena = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'registro'


class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True) # <-- Agregado porque lo usas en views
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    registro = models.OneToOneField(Registro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'usuario'


class Administradores(models.Model):
    id_admin = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'administradores'


class Amistad(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    usuario1 = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True, related_name='amistades_enviadas')
    usuario2 = models.ForeignKey(Usuario, models.DO_NOTHING, related_name='amistades_recibidas', blank=True, null=True)

    class Meta:
        db_table = 'amistad'


class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    sinopsis = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    archivo_pdf = models.TextField(blank=True, null=True)  # <-- Cambiado a TextField para aguantar el texto largo del editor

    class Meta:
        db_table = 'libro'


class AutorLibro(models.Model):
    id = models.BigAutoField(primary_key=True)
    rol = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    libro = models.ForeignKey(Libro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'autor_libro'


class Biblioteca(models.Model):
    id_biblioteca = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    fecha_agregado = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    libro = models.ForeignKey(Libro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'biblioteca'


class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'chat'


class ChatUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    chat = models.ForeignKey(Chat, models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'chat_usuario'


class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    contenido = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    libro = models.ForeignKey(Libro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'comentario'


class Interaccion(models.Model):
    id_interaccion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    libro = models.ForeignKey(Libro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'interaccion'


class LogAdmin(models.Model):
    id_log = models.AutoField(primary_key=True)
    accion = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    admin = models.ForeignKey(Administradores, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'log_admin'


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    contenido = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    chat = models.ForeignKey(Chat, models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'mensaje'


class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    leida = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'notificacion'


class Perfil(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    redes_sociales = models.TextField(blank=True, null=True)
    usuario = models.OneToOneField(Usuario, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'perfil'


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    motivo = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    interaccion = models.ForeignKey(Interaccion, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'reporte'


class Resena(models.Model):
    id_resena = models.AutoField(primary_key=True)
    comentario = models.TextField(blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, blank=True, null=True)
    libro = models.ForeignKey(Libro, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'resena'