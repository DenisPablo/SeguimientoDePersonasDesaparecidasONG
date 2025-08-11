from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import PersonaDesaparecida, User, Imagen, Ubicacion, UbicacionPista, Pista, Reporte, ImagenPista
from django.shortcuts import get_object_or_404
# Create your tests here.

# Testeo de mmodelos.
class ImagenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',   password='12345')
        
    def test_link_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen = Imagen(link='', usuario=self.user)
            imagen.full_clean()  # dispara las validaciones del modelo
        self.assertIn('link', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen = Imagen(link='http://example.com/image.jpg', usuario=None)
            imagen.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        imagen = Imagen(
            link='http://example.com/image.jpg',
            usuario=self.user 
                        )
        try:
            imagen.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
       
class PistaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        self.reporte = Reporte.objects.create(
            persona_desaparecida=PersonaDesaparecida.objects.create(
                nombre='Persona',
                apellido='Apellido',
                nro_documento='12345678',
                genero=1,
                fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
                estado_salud='Saludable',
                descripcion='Descripción de la persona desaparecida',
                imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
                nro_calzado=42,
                altura=1.75,
                peso=70.0,
                fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
                usuario=self.user
            ),
            descripcion='Descripción del reporte',
            usuario=self.user,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista',reporte=self.reporte, usuario=self.user)

    def test_descripcion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            pista = Pista(descripcion='', usuario=self.user)
            pista.full_clean()
        self.assertIn('descripcion', cm.exception.message_dict)
    
    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            pista = Pista(descripcion='Descripción de la pista',reporte= self.reporte , usuario=None)
            pista.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        pista = Pista(
            descripcion='Descripción de la pista',
            reporte=self.reporte,
            usuario=self.user
        )
        try:
            pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

class UbicacionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    '''
    def test_latitud_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=None, longitud=0.0, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('latitud', cm.exception.message_dict)

    def test_longitud_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=0.0, longitud=None, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('longitud', cm.exception.message_dict)
    '''

    def test_latitud_valida_inferior(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=-100, longitud=0.0, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('latitud', cm.exception.message_dict)

    def test_latitud_valida_superior(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=100.0, longitud=0.0, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('latitud', cm.exception.message_dict)

    def test_longitud_valida_inferior(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=0.0, longitud=-200.0, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('longitud', cm.exception.message_dict)

    def test_longitud_valida_superior(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=0.0, longitud=200.0, usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('longitud', cm.exception.message_dict)

    def test_descripcion_no_vacia(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=0.0, longitud=0.0, descripcion='', usuario=self.user)
            ubicacion.full_clean()
        self.assertIn('descripcion', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion = Ubicacion(latitud=0.0, longitud=0.0, usuario=None)
            ubicacion.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        ubicacion = Ubicacion(
            latitud=0.0,
            longitud=0.0,
            descripcion='Ubicación de prueba',
            usuario=self.user
        )
        try:
            ubicacion.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

class UbicacionPistaModelTest(TestCase):    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.persona = PersonaDesaparecida(
            nombre='Persona',
            apellido='Apellido',
            nro_documento='12345678',
            genero=1,
            fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
            estado_salud='Saludable',
            descripcion='Descripción de la persona desaparecida',
            imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
            nro_calzado=42,
            altura=1.75,
            peso=70.0,
            fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
            usuario=self.user
        )
        self.persona.save()  # Guardar la persona antes de crear el reporte
        # Crear un reporte asociado a la persona
        self.reporte = Reporte.objects.create(
            persona_desaparecida=self.persona,  # Asumiendo que no se requiere una persona para este test
            descripcion='Descripción del reporte',
            usuario=self.user,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista',reporte=self.reporte ,usuario=self.user)
        self.ubicacion = Ubicacion.objects.create(latitud=0.0, longitud=0.0, usuario=self.user)

    def test_ubicacion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion_pista = UbicacionPista(ubicacion=None, pista=self.pista, usuario=self.user)
            ubicacion_pista.full_clean()
        self.assertIn('ubicacion', cm.exception.message_dict)

    def test_pista_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion_pista = UbicacionPista(ubicacion=self.ubicacion, pista=None, usuario=self.user)
            ubicacion_pista.full_clean()
        self.assertIn('pista', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion_pista = UbicacionPista(ubicacion=self.ubicacion, pista=self.pista, usuario=None) 
            ubicacion_pista.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        ubicacion_pista = UbicacionPista(
            ubicacion=self.ubicacion,
            pista=self.pista,
            usuario=self.user
        )
        try:
            ubicacion_pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

class ImagenPistaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reporte = Reporte.objects.create(
            persona_desaparecida=PersonaDesaparecida.objects.create(
                nombre='Persona',
                apellido='Apellido',
                nro_documento='12345678',
                genero=1,
                fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
                estado_salud='Saludable',
                descripcion='Descripción de la persona desaparecida',
                imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
                nro_calzado=42,
                altura=1.75,
                peso=70.0,
                fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
                usuario=self.user
            ),
            descripcion='Descripción del reporte',
            usuario=self.user,
        )
        # Crear una pista asociada al reporte
        self.pista = Pista.objects.create(descripcion='Descripción de la pista',reporte=self.reporte, usuario=self.user)
        self.imagen = Imagen.objects.create(link='http://example.com/image.jpg', usuario=self.user)

    def test_imagen_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=None, pista=self.pista, usuario=self.user)
            imagen_pista.full_clean()
        self.assertIn('imagen', cm.exception.message_dict)

    def test_pista_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=self.imagen, pista=None, usuario=self.user)
            imagen_pista.full_clean()
        self.assertIn('pista', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=self.imagen, pista=self.pista, usuario=None)
            imagen_pista.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        imagen_pista = ImagenPista(
            imagen=self.imagen,
            pista=self.pista,
            usuario=self.user
        )
        try:
            imagen_pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

class ReporteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.persona_desaparecida = PersonaDesaparecida(
            nombre='Persona',
            apellido='Apellido',
            nro_documento='12345678',
            genero=1,
            fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
            estado_salud='Saludable',
            descripcion='Descripción de la persona desaparecida',
            imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
            nro_calzado=42,
            altura=1.75,
            peso=70.0,
            fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
            usuario=self.user
        )
        self.persona_desaparecida.save()

    def test_persona_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            reporte = Reporte(persona_desaparecida=None, descripcion='Descripción del reporte', usuario=self.user)
            reporte.full_clean()
        self.assertIn('persona_desaparecida', cm.exception.message_dict)

    def test_descripcion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            reporte = Reporte(persona_desaparecida=self.persona_desaparecida, descripcion='', usuario=self.user)
            reporte.full_clean()
        self.assertIn('descripcion', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            reporte = Reporte(persona_desaparecida=self.persona_desaparecida, descripcion='Descripción del reporte', usuario=None)
            reporte.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        reporte = Reporte(
            persona_desaparecida=self.persona_desaparecida,
            descripcion='Descripción del reporte',
            usuario=self.user,
            fecha_creacion=timezone.now()
        )
        try:
            reporte.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

class PersonaDesaparecidaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_nombre_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='', usuario=self.user)
            persona.full_clean()
        self.assertIn('nombre', cm.exception.message_dict)

    def test_nombre_normalizado(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', usuario=self.user)
            persona.full_clean()
        self.assertIn('nombre', cm.exception.message_dict)

    def test_apellido_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='', usuario=self.user)
            persona.full_clean()
        self.assertIn('apellido', cm.exception.message_dict)

    def test_apellido_normalizado(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', usuario=self.user)
            persona.full_clean()
        self.assertIn('apellido', cm.exception.message_dict)

    def test_nro_documento_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='', usuario=self.user)
            persona.full_clean()
        self.assertIn('nro_documento', cm.exception.message_dict)
    
    def test_nro_documento_formato(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='0123456789', usuario=self.user)
            persona.full_clean()
        self.assertIn('nro_documento', cm.exception.message_dict)

    def test_genero_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', genero=4, usuario=self.user)
            persona.full_clean()
        self.assertIn('genero', cm.exception.message_dict)

    def test_fecha_nacimiento_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=None, usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_nacimiento', cm.exception.message_dict)
    
    def test_fecha_nacimiento_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=timezone.now() + timezone.timedelta(days=1), usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_nacimiento', cm.exception.message_dict)

    def test_fecha_desaparicion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=None, usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_fecha_desaparicion_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=timezone.now() + timezone.timedelta(days=1), usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)
    
    def test_nro_calzado_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', nro_calzado=-1, usuario=self.user)
            persona.full_clean()
        self.assertIn('nro_calzado', cm.exception.message_dict)

    def test_fecha_desaparicion_no_futura(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=timezone.now() + timezone.timedelta(days=1), usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_fecha_desaparicion_no_anterior_nacimiento(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=timezone.now(), fecha_desaparicion=timezone.now() - timezone.timedelta(days=364), usuario=self.user)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_altura_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', altura=-1.0, usuario=self.user)
            persona.full_clean()
        self.assertIn('altura', cm.exception.message_dict)

    def test_peso_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', peso=-1.0, usuario=self.user)
            persona.full_clean()
        self.assertIn('peso', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', usuario=None)
            persona.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        persona = PersonaDesaparecida(
            nombre='Persona',
            apellido='Apellido',
            nro_documento='12345678',
            genero=1,
            fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
            estado_salud='Saludable',
            descripcion='Descripción de la persona desaparecida',
            imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
            nro_calzado=42,
            altura=1.75,
            peso=70.0,
            fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
            usuario=self.user
        )
        try:
            persona.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")

# Testeo de camino feliz,

class testeoFeliz(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.persona = PersonaDesaparecida(
            nombre='Persona',
            apellido='Apellido',
            nro_documento='12345678',
            genero=1,
            fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),  # 30 años atrás
            estado_salud='Saludable',
            descripcion='Descripción de la persona desaparecida',
            imagen_perfil=None,  # Asumiendo que no se proporciona una imagen
            nro_calzado=42,
            altura=1.75,
            peso=70.0,
            fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),  # Desapareció ayer
            usuario=self.user
        )
        
        self.persona.save();
    
        # Crear un reporte asociado a la persona
        self.reporte = Reporte.objects.create(
            persona_desaparecida=self.persona,
            descripcion='Descripción del reporte',
            usuario=self.user,
        )
        

        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.user)


        self.ubicacionPista = UbicacionPista.objects.create(
            ubicacion=Ubicacion.objects.create(latitud=0.0, longitud=0.0, usuario=self.user),
            pista=self.pista,
            usuario=self.user
        )


        self.ImagenPista = ImagenPista.objects.create(
            imagen=Imagen.objects.create(link='http://example.com/image.jpg', usuario=self.user),
            pista=self.pista,
            usuario=self.user
        )

    def test_creacion_exitosa(self):
    
        self.assertEqual(PersonaDesaparecida.objects.count(), 1)
        self.assertEqual(Reporte.objects.count(), 1)
        self.assertEqual(Pista.objects.count(), 1)
        self.assertEqual(UbicacionPista.objects.count(), 1)
        self.assertEqual(ImagenPista.objects.count(), 1)
        
    def test_obtener_reporte_completo(self):
        reporte = get_object_or_404(
            Reporte.objects.select_related('persona_desaparecida', 'usuario')
            .prefetch_related(
                'pistas',
                'pistas__ubicaciones_pista',
                'pistas__imagenes_pista',
                'pistas__ubicaciones_pista__ubicacion',
                'pistas__imagenes_pista__imagen'
            ),
            id=self.reporte.id,
            estado=True
        )

        self.assertEqual(reporte.id, self.reporte.id)
        self.assertEqual(reporte.persona_desaparecida.nombre, 'persona')  # recuerda que guardas en minúsculas

        pistas = list(reporte.pistas.all())
        self.assertEqual(len(pistas), 1)
        self.assertEqual(pistas[0].descripcion, 'Descripción de la pista')

        ubicaciones = list(pistas[0].ubicaciones_pista.all())
        self.assertEqual(len(ubicaciones), 1)
        self.assertAlmostEqual(ubicaciones[0].ubicacion.latitud, 0.0)

        imagenes = list(pistas[0].imagenes_pista.all())
        self.assertEqual(len(imagenes), 1)
        self.assertEqual(imagenes[0].imagen.link, 'http://example.com/image.jpg')
