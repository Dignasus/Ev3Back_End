from django.db import models
from django.contrib.auth.models import User

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class AsignacionPermiso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)