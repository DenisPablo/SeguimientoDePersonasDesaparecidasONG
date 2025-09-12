from django.shortcuts import get_object_or_404
from ..models import Imagen,Usuario

class ImagenServicio:
    
    @staticmethod
    def crear_imagen(imagen_obj):
        
        usuario = get_object_or_404(Usuario, id=imagen_obj.usuario_id)

        imagen = Imagen.objects.create(
            usuario = usuario,   # relacion con User
            descripcion = imagen_obj.descripcion,
            imagen = imagen_obj.imagen,
            estado = imagen_obj.estado,
        )

        return imagen
    @staticmethod
    def obtener_imagen_por_id(imagen_id):
        imagen = get_object_or_404(Imagen, id=imagen_id)
        
        return imagen
    
    @staticmethod
    def actualizar_imagen(imagen_id, imagen_nueva):
        imagen = get_object_or_404(Imagen, id=imagen_id)
        
        imagen.descripcion = imagen_nueva.descripcion
        imagen.imagen = imagen_nueva.imagen
        imagen.save()
        
        return imagen
    
    @staticmethod
    def activar_imagen(imagen_id):
        imagen = get_object_or_404(Imagen, id=imagen_id)
        imagen.estado = True
        imagen.save()

        return imagen
    
    @staticmethod
    def desactivar_imagen(imagen_id):
        imagen = get_object_or_404(Imagen, id=imagen_id)
        imagen.estado = False
        imagen.save()
        return imagen