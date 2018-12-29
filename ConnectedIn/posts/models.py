from django.db import models
from perfis.models import * 
class Post(models.Model):
    user = models.ForeignKey(Perfil, related_name='postagens', on_delete=models.DO_NOTHING)
    postagem = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
    	return self.postagem

    class Meta:
        ordering = ('-created_at',)
