from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import *

router = DefaultRouter()
router.register(r'usuarios', UsuarioSistemaViewSet, basename='usuarios')
router.register(r'ciudadanos', CiudadanoViewSet, basename='ciudadanos')
router.register(r'inventario', InventarioViewSet, basename='inventario')
router.register(r'visitas', BitacoraVisitaViewSet, basename='visitas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('api/login/', CustomLoginView.as_view(), name='api_login'),
]