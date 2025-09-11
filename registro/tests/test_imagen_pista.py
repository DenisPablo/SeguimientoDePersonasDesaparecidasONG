from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import ImagenPista, Imagen, Pista, PersonaDesaparecida, Reporte, User

class ImagenPistaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reporte = Reporte.objects.create(
            persona_desaparecida=PersonaDesaparecida.objects.create(
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
                usuario=self.user
            ),
            descripcion='Descripción del reporte',
            usuario=self.user,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.user)
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
