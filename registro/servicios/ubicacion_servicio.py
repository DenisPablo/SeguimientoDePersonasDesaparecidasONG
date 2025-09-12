from ..models import Ubicacion, Usuario
from django.shortcuts import get_object_or_404

class UbicacionServicio:
    def crear_ubicacion(ubicacion_obj):

        get_object_or_404(Usuario, id=ubicacion_obj.usuario.id)

        ubicacion = Ubicacion.objects.create(
            descripcion=ubicacion_obj.descripcion,
            latitud=ubicacion_obj.latitud,
            longitud=ubicacion_obj.longitud,
            usuario=ubicacion_obj.usuario,
            estado=ubicacion_obj.estado,
        )

        return ubicacion

    def obtener_detalles(self):
        ubicacion = Ubicacion.objects.get(id=self.ubicacion_id)

        return ubicacion
    
    def actualizar_ubicacion(ubicacion_id, ubicacion_nueva):
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        ubicacion.descripcion = ubicacion_nueva.descripcion.descripcion
        ubicacion.latitud = ubicacion_nueva.latitud
        ubicacion.longitud = ubicacion_nueva.longitud

        ubicacion.save()
        return ubicacion
    
    def desactivar_ubicacion(ubicacion_id):
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        ubicacion.estado = False
        ubicacion.save()
        return ubicacion
    
    def activar_ubicacion(ubicacion_id):
        ubicacion = Ubicacion.objects.get(id=ubicacion_id)
        ubicacion.estado = True
        ubicacion.save()
        return ubicacion