from rest_framework import viewsets
from .models import BitacoraVisita, Inventario, UsuarioSistema, Ciudadano
from .serializers import BitacoraVisitaSerializer, InventarioSerializer, UsuarioSistemaSerializer, CiudadanoSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UsuarioSistemaViewSet(viewsets.ModelViewSet):
    """
    Endpoints para la gestión de usuarios internos y roles (HU-06).
    Permite listar, crear, actualizar y eliminar personal del Punto Digital.
    """
    queryset = UsuarioSistema.objects.all().order_by('-id')
    serializer_class = UsuarioSistemaSerializer


class CiudadanoViewSet(viewsets.ModelViewSet):
    """
    Endpoints para el registro único de ciudadanos beneficiarios (HU-01).
    """
    queryset = Ciudadano.objects.all().order_by('-id')
    serializer_class = CiudadanoSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    """
    Endpoints automatizados para el control de infraestructura tecnológica (HU-02).
    """
    queryset = Inventario.objects.all().order_by('-id')
    serializer_class = InventarioSerializer

class BitacoraVisitaViewSet(viewsets.ModelViewSet):
    """
    Endpoints automatizados para el Registro de Visitas y Bitácora Diaria (HU-07).
    """
    queryset = BitacoraVisita.objects.all().order_by('-fecha_ingreso')
    serializer_class = BitacoraVisitaSerializer

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Aquí mandamos los datos clave al Frontend
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'is_staff': user.is_staff  # True o False
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)