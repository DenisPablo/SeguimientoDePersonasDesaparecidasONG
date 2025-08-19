from django.contrib.auth import authenticate, login, logout

class AuthService:
    
    @staticmethod
    def login_usuario(request, username: str, password: str):
        """
        Autentica al usuario y establece la sesión.
        """
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return user
        else:
            return None  # O lanzar excepción personalizada
    
    @staticmethod
    def logout_usuario(request):
        """
        Cierra la sesión del usuario actual.
        """
        logout(request)
    
    @staticmethod
    def obtener_usuario_actual(request):
        """
        Devuelve el usuario actualmente logueado a partir del request.
        """
        if request.user.is_authenticated:
            return request.user
        return None

    @staticmethod
    def obtener_usuario_id_actual(request):
        """
        Devuelve el ID del usuario logueado, útil para pasar a otros servicios.
        """
        usuario = AuthService.obtener_usuario_actual(request)
        return usuario.id if usuario else None
