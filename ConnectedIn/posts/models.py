from django.contrib.auth.models import User
from django.contrib.auth import *
from django.db import models

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
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



class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Perfil, related_name='comment', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.content

class Reaction(models.Model):
    GOSTEI = 'GO'
    HORRIVEL ='HR'
    QUERO = 'QR'
    LEGAL = 'LG'
    VOU = 'VU'
    VAMOS = 'VM'
    BOM = 'BM'
    OTIMO = 'OT'
    NAO = 'NO'
    REACTION=(
         (GOSTEI,'Gostei'),(VAMOS,'Vamos'),
         (HORRIVEL,'Horrivel'),(QUERO,'Quero'),
         (LEGAL,'Legal'),(VOU,'Vou'),
         (BOM,'Bom'),(OTIMO,'Otimo'),(NAO,'Nao'),
        )
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(Perfil, related_name='reaction', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=2, choices=REACTION, default=GOSTEI)
    reaction_date = models.DateTimeField(auto_now_add=True)