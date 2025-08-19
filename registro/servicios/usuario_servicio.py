from ..models import Usuario
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction

class UsuarioService:
    @staticmethod
    def actualizar_usuario(usuario_id, usuario_nuevo):
        """
        Actualiza la información del usuario y su perfil asociado usando una instancia de Usuario.
        usuario_nuevo: instancia de Usuario con los datos validados.
        """
        usuario = get_object_or_404(Usuario, id=usuario_id)
        user = usuario.user

        with transaction.atomic():
        # Actualizar campos del modelo User
            user.username = usuario_nuevo.user.username
            user.email = usuario_nuevo.user.email
            user.is_active = usuario_nuevo.user.is_active
            user.save()
            # Actualizar campos del modelo Usuario
            usuario.dni = usuario_nuevo.dni
            usuario.telefono = usuario_nuevo.telefono
            usuario.save()
            return usuario
    
    @staticmethod
    def obtener_usuario_id(usuario_id):
        return get_object_or_404(Usuario, id=usuario_id)
    
    @staticmethod
    def crear_usuario(usuario_obj):  

        user = User.objects.create_user(
            last_name=usuario_obj.user.last_name,
            first_name=usuario_obj.user.first_name,

            username=usuario_obj.user.username,
            password=usuario_obj.user.password,
            email=usuario_obj.user.email,

            is_active=usuario_obj.user.is_active,
        )
        
        usuario = Usuario.objects.create(
            user=user,
            dni = usuario_obj.dni,
            telefono = usuario_obj.telefono,
        ) 
      
        return usuario

    @staticmethod
    def desactivar_usuario(usuario_id):
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.user.is_active = False
        usuario.save()
        return usuario
    
    @staticmethod
    def activar_usuario(usuario_id):
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.user.is_active = True
        usuario.save()
        return usuario