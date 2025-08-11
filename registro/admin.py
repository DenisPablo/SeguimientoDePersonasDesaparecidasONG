from django.contrib import admin
from .models import PersonaDesaparecida, Reporte, Pista, Imagen, Ubicacion

admin.site.register(Pista)
admin.site.register(Imagen)
admin.site.register(Ubicacion)

@admin.register(PersonaDesaparecida)
class PersonaDesaparecidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'nro_documento', 'fecha_desaparicion', 'estado')
    search_fields = ('nombre', 'apellido', 'nro_documento')
    list_filter = ('genero', 'estado')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('persona_desaparecida', 'fecha_creacion', 'estado')
    search_fields = ('persona_desaparecida__nombre', 'persona_desaparecida__apellido')
    list_filter = ('estado',)

