from perfis import views
from django.urls import path
from django.contrib.auth import views as v
from usuarios.views import RegistrarUsuarioView

urlpatterns = [
	path('', views.index, name='index'),
	path('perfil/<int:perfil_id>', views.exibir_perfil, name='exibir'),
	path('perfil/<int:perfil_id>/convidar', views.convidar, name='convidar'),
	path('perfil/<int:perfil_id>/desfazer', views.desfazer, name='desfazer'),
	path('convite/<int:convite_id>/aceitar', views.aceitar, name='aceitar'),
	path('convite/<int:convite_id>/recusar', views.recusar, name='recusar'),
	path('login/', v.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
	path('logout/', v.LogoutView.as_view(template_name='usuarios/login.html'), name="logout"),
	path('registrar/', RegistrarUsuarioView.as_view(), name='registrar'),
	path('password/', views.change_password, name='change_password'),
	path('feed/', views.feed, name='feed'),
	path('promover/<int:perfil_id>', views.promover, name='promover'),
	path('desativar/',views.desativar, name='desativar'),
	path('reativar/',views.reativar, name='reativar'),
	path('bloquear/<int:perfil_id>',views.bloquear,name='bloquear'),
]