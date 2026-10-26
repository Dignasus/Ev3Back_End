from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from .models import Permiso, AsignacionPermiso

@extend_schema(
    request=inline_serializer(
        name='AutenticarRequest',
        fields={'username': serializers.CharField(), 'password': serializers.CharField()}
    )
)
@api_view(['POST'])
def autentificar(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        permisos = AsignacionPermiso.objects.filter(usuario=user).values_list('permiso__nombre', flat=True)
        menu = list(permisos) if permisos else ["Dashboard", "Perfil"]
        return Response({
            "autorizado": True,
            "usuario": user.username,
            "menu_opciones": menu
        }, status=status.HTTP_200_OK)
    
    return Response({"autorizado": False, "error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(
    request=inline_serializer(
        name='AgregarUsuarioRequest',
        fields={'username': serializers.CharField(), 'password': serializers.CharField()}
    )
)
@api_view(['POST'])
def agregarusuario(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "Faltan datos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
    
    User.objects.create_user(username=username, password=password)
    return Response({"mensaje": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)

@extend_schema(
    request=inline_serializer(
        name='ActualizarRequest',
        fields={'username': serializers.CharField(), 'new_password': serializers.CharField()}
    )
)
@api_view(['POST'])
def actualizar(request):
    username = request.data.get('username')
    new_password = request.data.get('new_password')
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return Response({"mensaje": "Contraseña actualizada exitosamente"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    request=inline_serializer(
        name='AddPermisoRequest',
        fields={'nombre': serializers.CharField()}
    )
)
@api_view(['POST'])
def addpermiso(request):
    nombre = request.data.get('nombre')
    if not nombre:
        return Response({"error": "Nombre de permiso requerido"}, status=status.HTTP_400_BAD_REQUEST)
    
    permiso, created = Permiso.objects.get_or_create(nombre=nombre)
    if created:
        return Response({"mensaje": "Permiso creado exitosamente"}, status=status.HTTP_201_CREATED)
    return Response({"mensaje": "El permiso ya existe"}, status=status.HTTP_200_OK)

@extend_schema(
    request=inline_serializer(
        name='AsociaPermisoRequest',
        fields={'username': serializers.CharField(), 'permiso_nombre': serializers.CharField()}
    )
)
@api_view(['POST'])
def asociapermiso(request):
    username = request.data.get('username')
    permiso_nombre = request.data.get('permiso_nombre')
    try:
        user = User.objects.get(username=username)
        permiso = Permiso.objects.get(nombre=permiso_nombre)
        AsignacionPermiso.objects.get_or_create(usuario=user, permiso=permiso)
        return Response({"mensaje": "Permiso asociado exitosamente al usuario"}, status=status.HTTP_200_OK)
    except (User.DoesNotExist, Permiso.DoesNotExist):
        return Response({"error": "Usuario o permiso no encontrado"}, status=status.HTTP_404_NOT_FOUND)