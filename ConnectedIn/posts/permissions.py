from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj.owner == request.user

class IsOwnerUpdate(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		try:
			perfil = Perfil.objects.get(id=view.kwargs['pk'])
		except:	
			return False
		if request.user.peril == perfil:
			return True
		return False
			
'''class IsOwnerUpdate(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return obj.owner == request.user'''