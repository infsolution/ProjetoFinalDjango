from django.db import models
from perfis.models import * 
class Post(models.Model):
    user = models.ForeignKey(Perfil, related_name='postagens', on_delete=models.DO_NOTHING)
    postagem = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    init = models.BooleanField(default=False)
    def __str__(self):
    	return self.postagem

    class Meta:
        ordering = ('-created_at',)


class Image(models.Model):
	post = models.ForeignKey(Post, related_name='imagens', on_delete=models.CASCADE)
	foto = models.ImageField(blank=True, null=True, upload_to='media/')
	