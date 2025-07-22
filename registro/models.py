from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Imagen(models.Model):
    ''' Modelo para guardar imagenes de personas y pruebas'''

    link = models.URLField(max_length=200, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes')
    # Relaciona la imagen con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"Imagen {self.id} - Usuario: {self.usuario.username}"

class Ubicacion(models.Model):
    ''' Modelo para guardar ubicaciones de personas y pruebas'''

    latitud = models.FloatField(null=False, blank=False)
    longitud = models.FloatField(null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ubicaciones')
    # Relaciona la ubicacion con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"Ubicación {self.id} - Usuario: {self.usuario.username}"

class UbicacionPista(models.Model):
    ''' Modelo para guardar ubicaciones de pistas de personas y pruebas'''
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.CASCADE, related_name='ubicaciones_pista')
    # Relaciona la ubicacion con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='ubicaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ubicaciones_pista')
    # Relaciona la ubicacion con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"UbicaciónPista {self.id} - Pista: {self.pista.id} - Usuario: {self.usuario.username}"

class ImagenPista(models.Model):
    ''' Modelo para guardar imagenes de pistas de personas y pruebas'''
    imagen = models.ForeignKey('Imagen', on_delete=models.CASCADE, related_name='imagenes_pista')
    # Relaciona la imagen con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='imagenes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes_pista')
    # Relaciona la imagen con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"ImagenPista {self.id} - Pista: {self.pista.id} - Usuario: {self.usuario.username}"
    

class Pista(models.Model):
    ''' Modelo para guardar pistas de personas y pruebas'''

    descripcion = models.TextField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un reporte
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"Pista {self.id} - Reporte: {self.reporte.id} - Usuario: {self.usuario.username}"

class PersonaDesaparecida(models.Model):
    ''' Modelo para guardar personas desaparecidas y pruebas'''

    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    nro_documento = models.CharField(max_length=20, null=True, blank=True)
    genero = models.CharField(max_length=10, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estado_salud = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    imagen_perfil = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='personas_desaparecidas', null=True, blank=True)
    nro_calzado = models.IntegerField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)

    fecha_desaparicion = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personas_desaparecidas')
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id})"

class Reporte(models.Model):
    ''' Modelo para guardar reportes de personas y pruebas'''

    descripcion = models.TextField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    persona_desaparecida = models.ForeignKey(PersonaDesaparecida, on_delete=models.CASCADE, related_name='reportes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes')
    # Relaciona el reporte con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    def __str__(self):
        return f"Reporte {self.id} - Persona: {self.persona_desaparecida.nombre} {self.persona_desaparecida.apellido} - Usuario: {self.usuario.username}"