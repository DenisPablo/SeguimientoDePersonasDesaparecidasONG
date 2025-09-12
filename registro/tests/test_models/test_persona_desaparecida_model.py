from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ...models import PersonaDesaparecida, User, Usuario

class PersonaDesaparecidaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            user=User.objects.create_user(username='testuser', password='12345'),
            dni='12345678',
            telefono='1234567890',
        )

    def test_nombre_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('nombre', cm.exception.message_dict)

    def test_nombre_normalizado(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('nombre', cm.exception.message_dict)

    def test_apellido_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('apellido', cm.exception.message_dict)

    def test_apellido_normalizado(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('apellido', cm.exception.message_dict)

    def test_nro_documento_requerido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('nro_documento', cm.exception.message_dict)
    
    def test_nro_documento_formato(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='0123456789', usuario=self.usuario)
            persona.full_clean()
        self.assertIn('nro_documento', cm.exception.message_dict)

    def test_genero_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', genero=4, usuario=self.usuario)
            persona.full_clean()
        self.assertIn('genero', cm.exception.message_dict)

    def test_fecha_nacimiento_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=None, usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_nacimiento', cm.exception.message_dict)
    
    def test_fecha_nacimiento_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=timezone.now() + timezone.timedelta(days=1), usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_nacimiento', cm.exception.message_dict)

    def test_fecha_desaparicion_requerida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=None, usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_fecha_desaparicion_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=timezone.now() + timezone.timedelta(days=1), usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)
    
    def test_nro_calzado_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', nro_calzado=-1, usuario=self.usuario)
            persona.full_clean()
        self.assertIn('nro_calzado', cm.exception.message_dict)

    def test_fecha_desaparicion_no_futura(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_desaparicion=timezone.now() + timezone.timedelta(days=1), usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_fecha_desaparicion_no_anterior_nacimiento(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', fecha_nacimiento=timezone.now(), fecha_desaparicion=timezone.now() - timezone.timedelta(days=364), usuario=self.usuario)
            persona.full_clean()
        self.assertIn('fecha_desaparicion', cm.exception.message_dict)

    def test_altura_valida(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', altura=-1.0, usuario=self.usuario)
            persona.full_clean()
        self.assertIn('altura', cm.exception.message_dict)

    def test_peso_valido(self):
        with self.assertRaises(ValidationError) as cm:
            persona = PersonaDesaparecida(nombre='Persona 1', apellido='Apellido 1', nro_documento='12345678', peso=-1.0, usuario=self.usuario)
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
        try:
            persona.full_clean()
        except ValidationError:
            self.fail("full_clean() debería pasar sin errores con datos válidos")
