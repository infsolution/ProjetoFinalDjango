from posts import views
from django.urls import path
urlpatterns = [
	path('add/<int:perfil_id>/',views.add, name='add'),
	path('delete/<int:post_id>', views.delete, name='delete'),
]