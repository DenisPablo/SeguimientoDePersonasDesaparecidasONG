from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import Imagen, Usuario, User

class ImagenModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345', last_name='Test', first_name='User', email="test@test.com"),
            dni='12345678',
            telefono='1234567890',
        )

    def test_imagen_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen = Imagen(imagen=None, usuario=self.usuario, descripcion='Imagen de prueba', estado=True)
            imagen.full_clean()
        self.assertIn('imagen', cm.exception.message_dict)

    def test_usuario_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            imagen = Imagen(imagen="path/to/image.jpg", descripcion = "test", usuario=None, estado=True)
            imagen.full_clean()
        self.assertIn('usuario', cm.exception.message_dict)

    def test_creacion_exitosa(self):
        imagen = Imagen.objects.create(
        imagen="imagenes/test.jpg",
        descripcion='Imagen de prueba',
        estado=True,
        usuario=self.usuario
        )   
        
        try:
            imagen.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
            self.assertEqual(imagen.usuario, self.usuario)
            self.assertEqual(imagen.descripcion, 'Imagen de prueba')
            self.assertTrue(imagen.estado)
            self.assertIsNotNone(imagen.fecha_modificacion)

    def test_borrado_logico(self):
        imagen = Imagen.objects.create(
            imagen="imagenes/test.jpg",
            descripcion='Imagen de prueba',
            estado=True,
            usuario=self.usuario
        )
        imagen.estado = False
        imagen.save()
        self.assertFalse(imagen.estado)
        self.assertIsNotNone(imagen.fecha_modificacion)
