from django.contrib.auth.models import User
from rest_framework import serializers
from posts.permissions import *
from posts.models import *

class ImageSerializer(serializers.HyperlinkedModelSerializer):
	post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='postagem')
	class Meta:
		model = Image
		fields=('url', 'pk', 'post', 'foto')

class PostSerializer(serializers.HyperlinkedModelSerializer):
	imagens = ImageSerializer(many=True, read_only=True)
	user = serializers.SlugRelatedField(queryset=Perfil.objects.all(), slug_field='nome')
	class Meta:
		model = Post
		fields=('url', 'pk', 'user', 'postagem', 'created_at', 'imagens')

	def update(self, instance, validated_data):
		instance.user = validated_data.get('user', instance.user)
		instance.postagem = validated_data.get('postagem', instance.postagem)
		instance.save()
		return instance

class PerfilSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	class Meta:
		model = Perfil
		fields=('url','pk', 'nome', 'postagens', 'owner')
class UserPerfilSerializer(serializers.HyperlinkedModelSerializer):
	postagens = PostSerializer(many=True, read_only=True)
	class Meta:
		model = Perfil
		fields=('url', 'nome','postagens','owner')
class UserSerializer(serializers.HyperlinkedModelSerializer):
	perfil = UserPerfilSerializer(many=False, read_only=True)
	class Meta:
		model=User
		fields=('url', 'pk', 'username', 'perfil')

class PostImageSerializers(serializers.HyperlinkedModelSerializer):
	imagens = ImageSerializer(many=True)
	class Meta:
		model=Post
		fields=('url','pk','user', 'postagem', 'imagens')
class PostCreateSerializers(serializers.HyperlinkedModelSerializer):
	user = serializers.SlugRelatedField(queryset=Perfil.objects.all(), slug_field='nome')
	class Meta:
		model = Post
		fields=('user', 'postagem', 'imagens')

class CommentSerializers(serializers.HyperlinkedModelSerializer):
	user = serializers.SlugRelatedField(queryset=Perfil.objects.all(), slug_field='nome')
	post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='postagem')
	class Meta:
		model=Comments
		fields = ('pk','url', 'post', 'user', 'content')