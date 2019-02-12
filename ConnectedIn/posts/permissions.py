from rest_framework import permissions
from .models import *
class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.owner == request.user

class IsOwnerUpdate(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method == 'GET':
			return True
		try:
			post = Post.objects.get(id=view.kwargs['pk'])
			print(type(post.user.owner))
		except:	
			return False
		if request.user == post.user.usuario:
			return True
		return False
			
'''class IsOwnerUpdate(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.owner == request.user'''