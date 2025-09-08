from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator
import unicodedata
import re
# Create your models here.

class Usuario(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    """
    Modelo que representa el perfil extendido de un usuario en el sistema.
    
    Atributos:
        user (User): Relación uno a uno con el usuario base de Django.
        dni (str): Documento Nacional de Identidad, único, entre 7 y 11 dígitos.
        telefono (str): Número de teléfono, único, entre 7 y 15 dígitos, puede ser nulo.
        fecha_creacion (datetime): Fecha de creación del registro de usuario.
        ultima_actualizacion (datetime): Fecha de la última actualización del registro.
    """
    dni_validator = RegexValidator(r'^\d{7,11}$', 'El DNI debe tener entre 7 y 11 dígitos numéricos')
    telefono_validator = RegexValidator(r'^\+?\d{7,15}$', 'Número de teléfono inválido')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    dni = models.CharField(max_length=11, unique=True, validators=[dni_validator])
    telefono = models.CharField(max_length=15,unique=True, null=True, blank=True, validators=[telefono_validator])

    fecha_creacion = models.DateTimeField(auto_now_add=True) 
    ultima_actualizacion = models.DateTimeField(auto_now=True)     

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"  

    @staticmethod
    def normalizar_nombre(nombre):
        if not nombre:
            return ''
        # Quitar espacios al inicio y fin, pasar a minúsculas
        nombre = nombre.strip().lower()
        # Normalizar unicode (NFD separa acentos)
        nombre = unicodedata.normalize('NFD', nombre)
        # Quitar acentos excepto la ñ
        nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn' or c == 'ñ')
        # Quitar puntuación (solo letras y ñ)
        nombre = re.sub(r'[^a-zñ\s]', '', nombre)
        return nombre

    def save(self, *args, **kwargs):
        if self.user.first_name:
            self.user.first_name = self.normalizar_nombre(self.user.first_name)
        if self.user.last_name:
            self.user.last_name = self.normalizar_nombre(self.user.last_name)
        
        self.user.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.username} - {self.dni}"
    

class Imagen(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar imágenes de personas y pruebas.
    Campos:
    - url: URL de la imagen
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''

    imagen = models.ImageField(upload_to='imagenes/', null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes')
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

    def __str__(self):
        return f"Imagen {self.id} - Usuario: {self.usuario.username}"

class Ubicacion(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar ubicaciones de personas y pruebas.
    Campos:
    - latitud: Latitud (-90 a 90)
    - longitud: Longitud (-180 a 180)
    - descripcion: Descripción opcional
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''

    latitud = models.FloatField(null=False, blank=False)
    longitud = models.FloatField(null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ubicaciones')
    # Relaciona la ubicacion con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return f"Ubicación {self.id} - Usuario: {self.usuario.username}"
    
    def clean(self):
        if not (-90 <= self.latitud <= 90):
            raise ValidationError({'latitud': 'La latitud debe estar entre -90 y 90.'})
        if not (-180 <= self.longitud <= 180):
            raise ValidationError({'longitud': 'La longitud debe estar entre -180 y 180.'})
        if self.descripcion is not None and self.descripcion.strip() == '':
            raise ValidationError({'descripcion': 'La descripción no puede estar vacía si se proporciona.'})

class UbicacionPista(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar ubicaciones de pistas de personas y pruebas.
    Campos:
    - ubicacion: Ubicación relacionada
    - pista: Pista relacionada
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.CASCADE, related_name='ubicaciones_pista')
    # Relaciona la ubicacion con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='ubicaciones_pista')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ubicaciones_pista')
    # Relaciona la ubicacion con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Ubicación de pista"
        verbose_name_plural = "Ubicaciones de pista"

    def __str__(self):
        return f"UbicaciónPista {self.id} - Pista: {self.pista.id} - Usuario: {self.usuario.username}"

class ImagenPista(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar imágenes de pistas de personas y pruebas.
    Campos:
    - imagen: Imagen relacionada
    - pista: Pista relacionada
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''
    imagen = models.ForeignKey('Imagen', on_delete=models.CASCADE, related_name='imagenes_pista')
    # Relaciona la imagen con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='imagenes_pista')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes_pista')
    # Relaciona la imagen con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Imagen de pista"
        verbose_name_plural = "Imágenes de pista"

    def __str__(self):
        return f"ImagenPista {self.id} - Pista: {self.pista.id} - Usuario: {self.usuario.username}"
    
class Pista(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar pistas de personas y pruebas.
    Campos:
    - descripcion: Descripción de la pista
    - fecha_creacion: Fecha de creación
    - reporte: Reporte relacionado
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''

    descripcion = models.TextField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un reporte
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Pista"
        verbose_name_plural = "Pistas"

    def __str__(self):
        return f"Pista {self.id} - Reporte: {self.reporte.id} - Usuario: {self.usuario.username}"

class PersonaDesaparecida(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar personas desaparecidas y pruebas.
    Campos:
    - nombre: Nombre
    - apellido: Apellido
    - nro_documento: Número de documento
    - genero: Género (1: Masculino, 2: Femenino, 3: Otro)
    - fecha_nacimiento: Fecha de nacimiento
    - estado_salud: Estado de salud
    - descripcion: Descripción
    - imagen_perfil: Imagen de perfil
    - nro_calzado: Número de calzado
    - altura: Altura
    - peso: Peso
    - fecha_desaparicion: Fecha y hora de desaparición
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''
    GENERO_CHOICES = (
        (1, 'Masculino'),
        (2, 'Femenino'),
        (3, 'Otro'),
    )
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    nro_documento = models.CharField(max_length=9, null=False, blank=False)
    genero = models.PositiveSmallIntegerField(choices=GENERO_CHOICES, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    estado_salud = models.TextField(max_length=200, null=False, blank=False)
    descripcion = models.TextField(null=False, blank=False)
    imagen_perfil = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='personas_desaparecidas', null=True, blank=True)
    nro_calzado = models.IntegerField(null=False, blank=False)
    altura = models.FloatField(null=False, blank=False)
    peso = models.FloatField(null=False, blank=False)
    fecha_desaparicion = models.DateTimeField(null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personas_desaparecidas')
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Persona desaparecida"
        verbose_name_plural = "Personas desaparecidas"

    def __str__(self):
        return f"{self.nombre} {self.apellido} (ID: {self.id})"
    
    def clean(self):
        import re
        now = timezone.now()
        errors = {}
        # Permitir letras y apóstrofes, pero NO espacios
        nombre = self.nombre.strip() if self.nombre else ''
        apellido = self.apellido.strip() if self.apellido else ''
        nombre_apellido_regex = r"^[A-Za-záéíóúüÜñÑ']+$"
        if not nombre or not re.match(nombre_apellido_regex, nombre):
            errors['nombre'] = 'El nombre solo puede contener letras y apóstrofes, sin espacios ni otros caracteres.'
        if not apellido or not re.match(nombre_apellido_regex, apellido):
            errors['apellido'] = 'El apellido solo puede contener letras y apóstrofes, sin espacios ni otros caracteres.'
        if self.fecha_nacimiento and self.fecha_nacimiento > now.date():
            errors['fecha_nacimiento'] = 'La fecha de nacimiento no puede ser futura.'
        if self.fecha_desaparicion and self.fecha_desaparicion > now:
            errors['fecha_desaparicion'] = 'La fecha y hora de desaparición no puede ser futura.'
        if self.fecha_nacimiento and self.fecha_desaparicion:
            nacimiento_min_datetime = timezone.datetime.combine(self.fecha_nacimiento, timezone.datetime.min.time())
            nacimiento_min_datetime = timezone.make_aware(nacimiento_min_datetime, timezone.get_current_timezone())
            if self.fecha_desaparicion < nacimiento_min_datetime:
                errors['fecha_desaparicion'] = 'La fecha y hora de desaparición no puede ser anterior a la fecha de nacimiento.'
        if self.nro_calzado is not None and self.nro_calzado <= 0:
            errors['nro_calzado'] = 'El número de calzado debe ser positivo.'
        if self.altura is not None and self.altura <= 0:
            errors['altura'] = 'La altura debe ser positiva.'
        if self.peso is not None and self.peso <= 0:
            errors['peso'] = 'El peso debe ser positivo.'
        if self.genero is not None and self.genero not in [1, 2, 3]:
            errors['genero'] = "El género debe ser 1 (Masculino), 2 (Femenino) o 3 (Otro)."
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        # Guarda nombre y apellido en minúsculas
        if self.nombre:
            self.nombre = self.nombre.strip().lower()
        if self.apellido:
            self.apellido = self.apellido.strip().lower()
        super().save(*args, **kwargs)
    def get_genero_display(self):
        return dict(self.GENERO_CHOICES).get(self.genero, '')

class Reporte(models.Model):
    fecha_modificacion = models.DateTimeField(auto_now=True)
    '''
    Modelo para guardar reportes de personas y pruebas.
    Campos:
    - descripcion: Descripción del reporte
    - fecha_creacion: Fecha de creación
    - fecha_modificacion: Fecha de modificación
    - persona_desaparecida: Persona desaparecida relacionada
    - usuario: Usuario relacionado
    - estado: Borrado lógico
    '''

    descripcion = models.TextField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    persona_desaparecida = models.ForeignKey(PersonaDesaparecida, on_delete=models.CASCADE, related_name='reportes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes')
    # Relaciona el reporte con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"

    def __str__(self):
        return f"Reporte {self.id} - Persona: {self.persona_desaparecida.nombre} {self.persona_desaparecida.apellido} - Usuario: {self.usuario.username}"