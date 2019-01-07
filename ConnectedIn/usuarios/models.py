# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Codigo(models.Model):
	user = models.ForeignKey(User, related_name='users',on_delete=models.CASCADE)
	date_send = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	code = models.CharField(max_length=512)
	def __str__(self):
		return self.code

