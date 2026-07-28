from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BitacoraVisita, UsuarioSistema, Ciudadano, Inventario

@admin.register(UsuarioSistema)
class UsuariosAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombre_completo', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'nombre_completo')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (('Información del Punto Digital', {'fields': ('nombre_completo', 'rol')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Información del Punto Digital', {'fields': ('nombre_completo', 'rol', 'email')}),)

@admin.register(Ciudadano)
class CiudadanoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'telefono', 'fecha_registro')
    search_fields = ('cedula', 'nombres', 'apellidos')
    list_filter = ('fecha_registro',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre_equipo', 'marca', 'estado', 'ubicacion')
    list_filter = ('estado', 'marca', 'ubicacion')
    search_fields = ('codigo', 'nombre_equipo')

@admin.register(BitacoraVisita)
class BitacoraVisitaAdmin(admin.ModelAdmin):
    list_display = ('ciudadano', 'facilitador', 'actividad', 'equipo_asignado', 'fecha_ingreso')
    list_filter = ('actividad', 'fecha_ingreso', 'facilitador')
    search_fields = ('ciudadano__cedula', 'ciudadano__nombres', 'ciudadano__apellidos')