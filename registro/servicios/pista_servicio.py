from ..models import Pista, Usuario
from django.shortcuts import get_object_or_404

class PistaServicio:
    
    @staticmethod
    def crear_pista(pista_obj):

        usuario = get_object_or_404(Usuario, id=pista_obj.usuario.id)

        pista= Pista.objects.create(
            usuario = usuario,
            descripcion = pista_obj.descripcion,
            reporte = pista_obj.reporte,
        )

        return pista
    
    @staticmethod
    def obtener_pista_id(pista_id):
        pista = get_object_or_404(Pista, id=pista_id)

        return pista
    
    @staticmethod
    def actualizar_pista(pista_obj):
        
        pista = get_object_or_404(Pista, id=pista_obj.id)

        pista.descripcion = pista_obj.descripcion
        pista.reporte = pista_obj.reporte

        pista.save()

        return pista
    
    @staticmethod
    def activar_pista(pista_id):
        pista = get_object_or_404(Pista, id=pista_id)

        pista.estado = True
        pista.save()

        return pista

    @staticmethod
    def desactivar_pista(pista_id):
        pista = get_object_or_404(Pista, id=pista_id)

        pista.estado = False
        
        pista.save()

        return pista