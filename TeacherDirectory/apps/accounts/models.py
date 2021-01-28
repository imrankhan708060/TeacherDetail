from datetime import date
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.files import File
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers

class Subject(models.Model):
    subject_name=models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, last_login=now)
        user.set_password(password)
        user.username = email
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)


# A user model which doesn't extend AbstractUser


class User(AbstractBaseUser, PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.
        Username and password are required. Other fields are optional.
        """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = PhoneNumberField(
        _("Phone number"),
        blank=True,
        null=True,
        help_text=_("In case we need to call you about your order")
    )
    avatar = models.ImageField(upload_to='users/avatars/', max_length=255, blank=True, null=True)
    room_number=models.CharField(max_length=50)
    subject = models.ManyToManyField(Subject,null=True,blank=True)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_name(self):
        """Return full name if available, else username."""
        full_name = self.get_full_name()
        if full_name != '':
            return full_name
        else:
            return self.username

    def get_absolute_url(self):
        return reverse("teacher-detail", kwargs={"pk": self.pk})



