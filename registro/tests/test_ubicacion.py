from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Ubicacion, User

class UbicacionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

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
