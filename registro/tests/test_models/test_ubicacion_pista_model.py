from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ...models import UbicacionPista, Ubicacion, Pista, PersonaDesaparecida, Reporte, User, Usuario

class UbicacionPistaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345'),
            dni='12345678',
            telefono='1234567890',
        )
        self.persona = PersonaDesaparecida.objects.create(
            nombre='Persona',
            apellido='Apellido',
            nro_documento='12345678',
            genero=1,
            fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),
            estado_salud='Saludable',
            descripcion='Descripción de la persona desaparecida',
            imagen_perfil=None,
            nro_calzado=42,
            altura=1.75,
            peso=70.0,
            fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),
            usuario=self.usuario
        )
        self.reporte = Reporte.objects.create(
            persona_desaparecida=self.persona,
            descripcion='Descripción del reporte',
            usuario=self.usuario,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.usuario)
        self.ubicacion = Ubicacion.objects.create(latitud=0.0, longitud=0.0, usuario=self.usuario)

    def test_ubicacion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion_pista = UbicacionPista(ubicacion=None, pista=self.pista, usuario=self.usuario)
            ubicacion_pista.full_clean()
        self.assertIn('ubicacion', cm.exception.message_dict)

    def test_pista_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            ubicacion_pista = UbicacionPista(ubicacion=self.ubicacion, pista=None, usuario=self.usuario)
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
            usuario=self.usuario
        )
        try:
            ubicacion_pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
