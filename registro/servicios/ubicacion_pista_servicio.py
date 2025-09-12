from ..models import UbicacionPista, Usuario
from django.shortcuts import get_object_or_404

class UbicacionPistaServicio():
    
    @staticmethod
    def crear_ubicacion_pista(ubicacion_obj, pista_obj):

        get_object_or_404(Usuario, id=pista_obj.usuario.id)

        ubicacion_pista = UbicacionPista.objects.create(
            ubicacion=ubicacion_obj,
            pista=pista_obj,
            usuario=pista_obj.usuario,
        )
        
        return ubicacion_pista
    
    @staticmethod
    def obtener_ubicacion_pista_id(ubicacion_pista_id):
        ubicacion_pista = get_object_or_404(UbicacionPista, id=ubicacion_pista_id)

        return ubicacion_pista
    
    @staticmethod
    def obtener_ubicacion_pista_por_pista(pista_id):
        ubicacion_pista = UbicacionPista.objects.filter(pista__id=pista_id, estado=True)
        
        return ubicacion_pista
    
    @staticmethod
    def desactivar_ubicacion_pista(ubicacion_pista_id):
        ubicacion_pista = get_object_or_404(UbicacionPista, id=ubicacion_pista_id)
        ubicacion_pista.estado = False
        ubicacion_pista.save()
        
        return ubicacion_pista
    
    @staticmethod
    def activar_ubicacion_pista(ubicacion_pista_id):
        ubicacion_pista = get_object_or_404(UbicacionPista, id=ubicacion_pista_id)
        ubicacion_pista.estado = True
        ubicacion_pista.save()
        
        return ubicacion_pista