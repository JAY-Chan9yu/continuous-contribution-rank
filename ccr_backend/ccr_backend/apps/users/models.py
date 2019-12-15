from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models


class User(auth_models.AbstractUser):
    name = models.CharField(verbose_name='name', max_length=50)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'user'

    def __str__(self):
        return "name: {}".format(self.username)


class UserGitHub(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=False, blank=False)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'user_github'
        verbose_name_plural = 'user_github'

    def __str__(self):
        return "name: {}/ address='{}'".format(self.user.username, self.address)
