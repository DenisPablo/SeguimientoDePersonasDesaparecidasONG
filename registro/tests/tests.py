from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import PersonaDesaparecida, User, Usuario, Imagen, Ubicacion, UbicacionPista, Pista, Reporte, ImagenPista
from django.shortcuts import get_object_or_404
# Create your tests here.


class testeoFeliz(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345',last_name='Apellido', first_name='persona',email="test@test.com")
        self.usuario = Usuario.objects.create(
            user=user,
            dni = "12345678",
            telefono='1234567890',
        )

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
            usuario=self.usuario
        )
        
        self.persona.save();
    
        # Crear un reporte asociado a la persona
        self.reporte = Reporte.objects.create(
            persona_desaparecida=self.persona,
            descripcion='Descripción del reporte',
            usuario=self.usuario,
        )
        

        self.pista = Pista.objects.create(descripcion='Descripción de la pista', reporte=self.reporte, usuario=self.usuario)


        self.ubicacionPista = UbicacionPista.objects.create(
            ubicacion=Ubicacion.objects.create(latitud=0.0, longitud=0.0, usuario=self.usuario),
            pista=self.pista,
            usuario=self.usuario
        )


        self.ImagenPista = ImagenPista.objects.create(
            imagen=Imagen.objects.create(imagen="path/to/image.jpg", descripcion = "imagen", usuario=self.usuario),
            pista=self.pista,
            usuario=self.usuario
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
        self.assertEqual(imagenes[0], self.ImagenPista)  # Verifica que la imagen sea la misma que creaste
