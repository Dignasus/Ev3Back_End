from django.urls import path
from .views import autentificar, agregarusuario, actualizar, addpermiso, asociapermiso

urlpatterns = [
    path('autentificar/', autentificar, name='autentificar'),
    path('agregarusuario/', agregarusuario, name='agregarusuario'),
    path('actualizar/', actualizar, name='actualizar'),
    path('addpermiso/', addpermiso, name='addpermiso'),
    path('asociapermiso/', asociapermiso, name='asociapermiso'),
]