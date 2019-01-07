from usuarios import views
from django.urls import path
from django.contrib.auth import views as v
from usuarios.views import RegistrarUsuarioView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reset_password/',views.reset, name='reset_password'),
    path('redefinir/<str:codigo>/', views.redefinir, name='redefinir'),
    path('confirmar_reset', views.confirmar_reset, name='confirm'),
]