from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ...models import Reporte, PersonaDesaparecida, User, Usuario

class ReporteModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345'),
            dni='12345678',
            telefono='1234567890',
        )
        self.persona_desaparecida = PersonaDesaparecida.objects.create(
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

    def test_persona_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            reporte = Reporte(persona_desaparecida=None, descripcion='Descripción del reporte', usuario=self.usuario)
            reporte.full_clean()
        self.assertIn('persona_desaparecida', cm.exception.message_dict)

    def test_descripcion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            reporte = Reporte(persona_desaparecida=self.persona_desaparecida, descripcion='', usuario=self.usuario)
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
            usuario=self.usuario,
            fecha_creacion=timezone.now()
        )
        try:
            reporte.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
