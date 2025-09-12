from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import Imagen, Usuario, User
from ...servicios import ImagenServicio 

class ImagenServicioTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345', last_name='Test', first_name='User', email="test@test.com"),
            dni='12345678',
            telefono='1234567890',
        )

    def test_crear_imagen_exitosamente(self):
        imagen_obj = Imagen(
            imagen="path/to/image.jpg",
            descripcion='Imagen de prueba',
            estado=True,
            usuario=self.usuario
        )
        imagen_creada = ImagenServicio.crear_imagen(imagen_obj)

        self.assertEqual(ImagenServicio.obtener_imagen_por_id(imagen_creada.id), imagen_creada)
        self.assertEqual(imagen_creada.imagen, "path/to/image.jpg")
        self.assertEqual(imagen_creada.descripcion, 'Imagen de prueba')
        self.assertEqual(imagen_creada.usuario, self.usuario)
        self.assertTrue(imagen_creada.estado)
    
    def test_actualizar_imagen_exitosamente(self):
        imagen_obj = Imagen(
            imagen="path/to/image.jpg",
            descripcion='Imagen de prueba',
            estado=True,
            usuario=self.usuario
        )

        imagenPrevia = ImagenServicio.crear_imagen(imagen_obj)

        nueva_imagen_obj = Imagen(
            imagen="path/to/new_image.jpg",
            descripcion='Nueva descripción',
            estado=False,
            usuario=self.usuario
        )

        imagen_actualizada = ImagenServicio.actualizar_imagen(imagenPrevia.id, nueva_imagen_obj)

        self.assertEqual(imagen_actualizada.imagen, "path/to/new_image.jpg")
        self.assertEqual(imagen_actualizada.descripcion, 'Nueva descripción')
        self.assertTrue(imagen_actualizada.estado)
        self.assertNotEqual(imagenPrevia.fecha_modificacion, imagen_actualizada.fecha_modificacion)  # Asegura que la fecha de modificación se actualizó

    def test_activar_desactivar_imagen(self):
        imagen_obj = Imagen(
            imagen="path/to/image.jpg",
            descripcion='Imagen de prueba',
            estado=True,
            usuario=self.usuario
        )

        imagen = ImagenServicio.crear_imagen(imagen_obj)

        # Desactivar la imagen
        imagen_desactivada = ImagenServicio.desactivar_imagen(imagen.id)
        self.assertFalse(imagen_desactivada.estado)

        # Activar la imagen
        imagen_activada = ImagenServicio.activar_imagen(imagen.id)
        self.assertTrue(imagen_activada.estado)