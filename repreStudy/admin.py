from django.contrib import admin
from .models import Representante, Alumno, RegistroEliminado

# para administrar mejor los modelos
class RepresentanteAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('nombres', 'apellidos', 'cedula')
    # para agregar un buscador
    search_fields = ('nombres', 'cedula', 'serial_patria', 'codigo_patria')
    # para añadir filtros
    list_filter = ('nombres', 'apellidos', 'cedula')

# para registrar el modelo y salga en el panel de admin
admin.site.register(Representante, RepresentanteAdmin)


# para administrar mejor los modelos
class AlumnoAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('nombres', 'apellidos', 'edad', 'sexo', 'grado_y_seccion')
    # para agregar un buscador
    search_fields = ('nombres', 'apellidos', 'edad', 'sexo', 'grado_y_seccion')
    # para añadir filtros
    list_filter = ('nombres', 'apellidos', 'grado_y_seccion')
    # gerarquia de fechas
    date_hierarchy = 'fecha_de_nacimiento'

admin.site.register(Alumno, AlumnoAdmin)


# para administrar mejor los modelos
class RegistroEliminadoAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('tipo', 'datos', 'eliminado_por', 'fecha_eliminacion')
    # para agregar un buscador
    search_fields = ('tipo', 'eliminado_por', 'fecha_eliminacion')
    # para añadir filtros
    list_filter = ('tipo', 'eliminado_por', 'fecha_eliminacion')
    # gerarquia de fechas
    date_hierarchy = 'fecha_eliminacion'

admin.site.register(RegistroEliminado, RegistroEliminadoAdmin)
