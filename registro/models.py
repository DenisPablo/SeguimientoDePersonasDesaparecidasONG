from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Imagen(models.Model):
    ''' Modelo para guardar imagenes de personas y pruebas'''

    link = models.URLField(max_length=200, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes')
    # Relaciona la imagen con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"

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
    ''' Modelo para guardar ubicaciones de pistas de personas y pruebas'''
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.CASCADE, related_name='ubicaciones_pista')
    # Relaciona la ubicacion con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='ubicaciones')
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
    ''' Modelo para guardar imagenes de pistas de personas y pruebas'''
    imagen = models.ForeignKey('Imagen', on_delete=models.CASCADE, related_name='imagenes_pista')
    # Relaciona la imagen con una pista
    pista = models.ForeignKey('Pista', on_delete=models.CASCADE, related_name='imagenes')
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
    ''' Modelo para guardar pistas de personas y pruebas'''

    descripcion = models.TextField(null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    reporte = models.ForeignKey('Reporte', on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un reporte
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pistas')
    # Relaciona la pista con un usuario
    estado = models.BooleanField(default=True)
    # True = activo, False = borrado lógico

    class Meta:
        verbose_name = "Pista"
        verbose_name_plural = "Pistas"

    def __str__(self):
        return f"Pista {self.id} - Reporte: {self.reporte.id} - Usuario: {self.usuario.username}"

class PersonaDesaparecida(models.Model):
    ''' Modelo para guardar personas desaparecidas y pruebas'''

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
    nro_calzado = models.IntegerField(max_length=2, null=False, blank=False)
    
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
        import unicodedata
        now = timezone.now()
        errors = {}
        # Normalización y limpieza de cadenas
        def normalize_str(s):
            if s is None:
                return ''
            s = s.strip()
            s = unicodedata.normalize('NFKC', s)
            return s
        nombre = normalize_str(self.nombre)
        apellido = normalize_str(self.apellido)
        # Validación de campos obligatorios
        if not nombre:
            errors['nombre'] = 'El nombre es obligatorio y no puede estar vacío ni contener solo espacios.'
        if not apellido:
            errors['apellido'] = 'El apellido es obligatorio y no puede estar vacío ni contener solo espacios.'
        # Validación de caracteres permitidos
        nombre_apellido_regex = r"^[A-Za-záéíóúÁÉÍÓÚüÜñÑ\-' ]+$"
        if nombre and not re.match(nombre_apellido_regex, nombre):
            errors['nombre'] = 'El nombre solo puede contener letras, espacios, guiones y apóstrofes.'
        if apellido and not re.match(nombre_apellido_regex, apellido):
            errors['apellido'] = 'El apellido solo puede contener letras, espacios, guiones y apóstrofes.'
        # Fecha de nacimiento no futura
        if self.fecha_nacimiento and self.fecha_nacimiento > now.date():
            errors['fecha_nacimiento'] = 'La fecha de nacimiento no puede ser futura.'
        # Fecha de desaparición no futura
        if self.fecha_desaparicion and self.fecha_desaparicion > now:
            errors['fecha_desaparicion'] = 'La fecha y hora de desaparición no puede ser futura.'
        # Fecha de desaparición no anterior a nacimiento
        if self.fecha_nacimiento and self.fecha_desaparicion:
            nacimiento_min_datetime = timezone.datetime.combine(self.fecha_nacimiento, timezone.datetime.min.time())
            nacimiento_min_datetime = timezone.make_aware(nacimiento_min_datetime, timezone.get_current_timezone())
            if self.fecha_desaparicion < nacimiento_min_datetime:
                errors['fecha_desaparicion'] = 'La fecha y hora de desaparición no puede ser anterior a la fecha de nacimiento.'
        # nro_calzado positivo
        if self.nro_calzado is not None and self.nro_calzado <= 0:
            errors['nro_calzado'] = 'El número de calzado debe ser positivo.'
        # altura positiva
        if self.altura is not None and self.altura <= 0:
            errors['altura'] = 'La altura debe ser positiva.'
        # peso positivo
        if self.peso is not None and self.peso <= 0:
            errors['peso'] = 'El peso debe ser positivo.'
        # género válido
        if self.genero is not None and self.genero not in [1, 2, 3]:
            errors['genero'] = "El género debe ser 1 (Masculino), 2 (Femenino) o 3 (Otro)."
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        import unicodedata
        # Normaliza y limpia antes de guardar
        if self.nombre:
            self.nombre = unicodedata.normalize('NFKC', self.nombre.strip())
        if self.apellido:
            self.apellido = unicodedata.normalize('NFKC', self.apellido.strip())
        super().save(*args, **kwargs)
    def get_genero_display(self):
        return dict(self.GENERO_CHOICES).get(self.genero, '')

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

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"

    def __str__(self):
        return f"Reporte {self.id} - Persona: {self.persona_desaparecida.nombre} {self.persona_desaparecida.apellido} - Usuario: {self.usuario.username}"