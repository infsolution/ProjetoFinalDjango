from posts import views
from django.urls import path, include
from rest_framework.authtoken import views as token
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
	path('add/<int:perfil_id>/',views.add, name='add'),
	path('delete/<int:post_id>/', views.delete, name='delete'),
	path('comment/<int:post_id>/', views.to_comment, name='comment'),
	path('reaction/<int:post_id>/',views.to_react, name='reaction'),
	path('share/<int:post_id>/', views.to_share, name='share'),
	path('api/posts/',views.PostList.as_view(), name=views.PostList.name),
	path('api/posts/<int:pk>/', views.PostDetail.as_view(), name=views.PostDetail.name),
	path('api/perfil/',views.PerfilList.as_view(), name=views.PerfilList.name),
	path('api/perfil/<int:pk>/', views.PerfilDetail.as_view(), name=views.PerfilDetail.name),
	path('api/image/',views.ImageList.as_view(), name=views.ImageList.name),
	path('api/image/<int:pk>/', views.ImageDetail.as_view(), name=views.ImageDetail.name),
	path('api/user/',views.UserList.as_view(), name=views.UserList.name),
	path('api/user/<int:pk>/', views.UserDetail.as_view(), name=views.UserDetail.name),
	path('api/post-create/',views.PostCreate.as_view(), name=views.PostCreate.name),
	path('api/comments/', views.CommentsList.as_view(), name=views.CommentsList.name),
	path('api/comments/<int:pk>/', views.CommentsDetail.as_view(), name=views.CommentsDetail.name),
	path('api-auth/', include('rest_framework.urls')),
	path('api/postimage/',views.PostImageList.as_view(), name=views.PostImageList.name),
	path('api-token-auth/', token.obtain_auth_token, name='api-token-auth'),
]