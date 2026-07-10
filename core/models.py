from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioSistema(AbstractUser):
    """
    Modelo extendido de Django para gestionar los usuarios internos (HU-06).
    """
    ROLES_CHOICES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('FACILITADOR', 'Facilitador'),
        ('TECNICO', 'Técnico de Soporte'),
        ('OPERADOR', 'Operador'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='OPERADOR')
    nombre_completo = models.CharField(max_length=255)
    
    REQUIRED_FIELDS = ['nombre_completo', 'email']

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"


class Ciudadano(models.Model):
    """
    Modelo optimizado basado en ciudadano.php con separación de apellidos y dirección.
    """
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cedula} - {self.nombres} {self.apellidos}"


class Inventario(models.Model):
    """
    Modelo de Inventario (HU-02) extraído de inventariocontroler.php
    """
    ESTADO_CHOICES = [
        ('BUENO', 'Bueno / Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('BAJA', 'De Baja / Inoperativo'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre_equipo = models.CharField(max_length=150)
    marca = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BUENO')
    ubicacion = models.CharField(max_length=150, help_text="Ej: Área de Capacitación, Recepción")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.codigo}] {self.nombre_equipo} - {self.marca}"
    
class BitacoraVisita(models.Model):
    """
    Modelo de Control de Visitas y Bitácora Diaria (HU-07).
    Relaciona al Ciudadano, el Facilitador que atiende y el Equipo utilizado.
    """
    ACTIVIDAD_CHOICES = [
        ('CAPACITACION', 'Capacitación / Curso'),
        ('TRAMITE', 'Trámite Ciudadano'),
        ('NAVEGACION', 'Navegación Libre / Internet'),
        ('SOPORTE', 'Asistencia Técnica / Consulta'),
    ]

    # Relaciones (Foreign Keys)
    ciudadano = models.ForeignKey(
        Ciudadano, 
        on_delete=models.CASCADE, 
        related_name='visitas',
        help_text="Ciudadano que asiste al Punto Digital"
    )
    facilitador = models.ForeignKey(
        UsuarioSistema, 
        on_delete=models.PROTECT, 
        related_name='visitas_atendidas',
        help_text="Personal que registra la visita"
    )
    equipo_asignado = models.ForeignKey(
        Inventario, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='usos',
        help_text="Equipo tecnológico prestado (opcional)"
    )

    # Información de la Visita
    actividad = models.CharField(max_length=30, choices=ACTIVIDAD_CHOICES)
    observaciones = models.TextField(blank=True, null=True, help_text="Detalle del trámite o tema de consulta")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visita de {self.ciudadano.nombres} - {self.get_actividad_display()} ({self.fecha_ingreso.strftime('%d/%m/%Y')})"