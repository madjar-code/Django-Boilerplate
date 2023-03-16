from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import\
    AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import\
    RefreshToken
from django_rest_passwordreset.signals import\
    reset_password_token_created
from common.mixins.models import UUIDModel
from .managers import UserManager


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,
                              unique=True,
                              db_index=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def tokens(self) -> dict:
        """
        Возврат токенов для пользователя.
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = '{}?token={}'.\
        format(reverse('password_reset:reset-password-request'),
               reset_password_token.key)
    
    send_mail(
        'Password Reset for {title}'.\
            format(title='Some website title'),
        email_plaintext_message,
        'madzhar_80@mail.ru',
        [reset_password_token.user.email]
    )