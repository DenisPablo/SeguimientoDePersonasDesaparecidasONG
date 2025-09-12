from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ...models import Pista, Reporte, PersonaDesaparecida, User, Usuario
from django.shortcuts import get_object_or_404
# Create your tests here.

class PistaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345'),
            dni='12345678',
            telefono='1234567890',
        )
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
                usuario=self.usuario
            ),
            descripcion='Descripción del reporte',
            usuario=self.usuario,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.usuario)

    def test_descripcion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            pista = Pista(descripcion='', usuario=self.usuario)
            pista.full_clean()
        self.assertIn('descripcion', cm.exception.message_dict)
    
    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            pista = Pista(descripcion='Descripción de la pista', reporte=self.reporte, usuario=None)
            pista.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        pista = Pista(
            descripcion='Descripción de la pista',
            reporte=self.reporte,
            usuario=self.usuario
        )
        try:
            pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")