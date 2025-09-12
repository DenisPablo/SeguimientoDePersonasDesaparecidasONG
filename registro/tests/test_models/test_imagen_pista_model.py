from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ...models import ImagenPista, Imagen, Pista, PersonaDesaparecida, Reporte, User, Usuario

class ImagenPistaModelTest(TestCase):
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
                fecha_nacimiento=timezone.now() - timezone.timedelta(days=365 * 30),
                estado_salud='Saludable',
                descripcion='Descripción de la persona desaparecida',
                imagen_perfil=None,
                nro_calzado=42,
                altura=1.75,
                peso=70.0,
                fecha_desaparicion=timezone.now() - timezone.timedelta(days=1),
                usuario=self.usuario
            ),
            descripcion='Descripción del reporte',
            usuario=self.usuario,
        )
        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.usuario)
        self.imagen = Imagen.objects.create(imagen='imagenes/test.jpg', usuario=self.usuario, descripcion='Imagen de pista', estado=True)

    def test_imagen_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=None, pista=self.pista, usuario=self.usuario)
            imagen_pista.full_clean()
        self.assertIn('imagen', cm.exception.message_dict)

    def test_pista_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=self.imagen, pista=None, usuario=self.usuario)
            imagen_pista.full_clean()
        self.assertIn('pista', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen_pista = ImagenPista(imagen=self.imagen, pista=self.pista, usuario=None)
            imagen_pista.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        imagen_pista = ImagenPista.objects.create(
            imagen=self.imagen,
            pista=self.pista,
            usuario=self.usuario,
            estado=True
        )
        try:
            imagen_pista.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
        self.assertEqual(imagen_pista.imagen, self.imagen)
        self.assertEqual(imagen_pista.pista, self.pista)
        self.assertEqual(imagen_pista.usuario, self.usuario)
        self.assertTrue(imagen_pista.estado)
        self.assertIsNotNone(imagen_pista.fecha_modificacion)

    def test_borrado_logico(self):
        imagen_pista = ImagenPista.objects.create(
            imagen=self.imagen,
            pista=self.pista,
            usuario=self.usuario,
            estado=True
        )
        imagen_pista.estado = False
        imagen_pista.save()
        self.assertFalse(imagen_pista.estado)
        self.assertIsNotNone(imagen_pista.fecha_modificacion)
