from ..models import Reporte, Usuario
from django.shortcuts import get_object_or_404

class ReporteServicio:

    @staticmethod
    def crear_reporte(reporte_obj):

        get_object_or_404(Usuario, id=reporte_obj.usuario.id)

        reporte = Reporte.objects.create(
            descripcion=reporte_obj.descripcion,
            Usuario=reporte_obj.usuario,
            estado=reporte_obj.estado,
        )

        return reporte
    
    @staticmethod
    def obtener_reporte_id(reporte_id):
        reporte = get_object_or_404(Reporte, id=reporte_id)

        return reporte
    
    @staticmethod
    def actualizar_reporte(reporte_id, reporte_nuevo):
        reporte = get_object_or_404(Reporte, id=reporte_id)
        reporte.descripcion = reporte_nuevo.descripcion
        reporte.save()
        return reporte  
    
    @staticmethod
    def desactivar_reporte(reporte_id):
        reporte = get_object_or_404(Reporte, id=reporte_id)
        reporte.estado = False
        reporte.save()
        return reporte
    
    def activar_reporte(reporte_id):
        reporte = get_object_or_404(Reporte, id=reporte_id)
        reporte.estado = True
        reporte.save()
        return reporte