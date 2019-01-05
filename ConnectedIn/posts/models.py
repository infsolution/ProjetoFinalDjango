from django.contrib.auth.models import User
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


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Tип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Member"))

    #@models.permalink
    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Message date'), default=timezone.now)
    is_readed = models.BooleanField(_('Readed'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message
