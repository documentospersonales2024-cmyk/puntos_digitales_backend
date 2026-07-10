from rest_framework import serializers
from .models import BitacoraVisita, UsuarioSistema, Ciudadano, Inventario

class UsuarioSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSistema
        fields = ['id', 'username', 'email', 'nombre_completo', 'rol', 'is_active', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CiudadanoSerializer(serializers.ModelSerializer):
    # Campo computado para no romper compatibilidad si el front pide el nombre unido
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Ciudadano
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'nombre_completo', 'telefono', 'direccion', 'fecha_registro']

    def get_nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class BitacoraVisitaSerializer(serializers.ModelSerializer):
    ciudadano_nombre = serializers.ReadOnlyField(source='ciudadano.nombres')
    ciudadano_apellido = serializers.ReadOnlyField(source='ciudadano.apellidos')
    ciudadano_cedula = serializers.ReadOnlyField(source='ciudadano.cedula')
    facilitador_nombre = serializers.ReadOnlyField(source='facilitador.nombre_completo')
    equipo_codigo = serializers.ReadOnlyField(source='equipo_assigned.codigo')

    class Meta:
        model = BitacoraVisita
        fields = [
            'id', 'ciudadano', 'ciudadano_cedula', 'ciudadano_nombre', 'ciudadano_apellido',
            'facilitador', 'facilitador_nombre', 'equipo_asignado', 'equipo_codigo',
            'actividad', 'observaciones', 'fecha_ingreso'
        ]