from django.db import models
from django.conf import settings
from django.contrib.sessions.models import (
    AbstractBaseSession,
    BaseSessionManager
)
from django.utils.translation import ugettext_lazy as _


class SessionManager(BaseSessionManager):
    """Session manager"""
    use_in_migrations = True

    def encode(self, session_dict):
        """Returns the given session dictionary serialized and encoded as a string."""
        return UserSessionStore().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        s = self.model(session_key, self.encode(session_dict), expire_date)
        if session_dict:
            s.save()
        else:
            s.delete()  # Clear sessions with no data.
        return s


class Session(AbstractBaseSession):
    """Session model
    containing user session information
    Additionally this session object provides the following properties:
    `user`, `user_agent`, `location`, `device`, `last_activity` and `ip`.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    user_agent = models.CharField(
        _('User Agent'),
        null=True,
        blank=True,
        max_length=200
    )
    last_activity = models.DateTimeField(
        _('Last Activity'),
        auto_now=True
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP')
    )
    location = models.CharField(
        _('Location'),
        max_length=50,
        null=True,
        blank=True
    )
    device_brand = models.CharField(
        _('Device Brand'),
        max_length=50,
        null=True,
        blank=True
    )
    device_model = models.CharField(
        _('Device Model'),
        max_length=50,
        null=True,
        blank=True
    )
    browser = models.CharField(
        _('Browser'),
        max_length=50,
        null=True,
        blank=True
    )
    browser_version = models.CharField(
        _('Browser Version'),
        max_length=50,
        null=True,
        blank=True
    )
    os = models.CharField(
        _('OS'),
        max_length=50,
        null=True,
        blank=True
    )
    os_version = models.CharField(
        _('OS Version'),
        max_length=50,
        null=True,
        blank=True
    )
    is_mobile = models.BooleanField(
        _('Is mobile'),
        default=False
    )
    is_tablet = models.BooleanField(
        _('Is tablet'),
        default=False
    )
    is_touch_capable = models.BooleanField(
        _('Is touch capable'),
        default=False
    )
    is_pc = models.BooleanField(
        _('Is pc'),
        default=False
    )
    is_bot = models.BooleanField(
        _('Is bot'),
        default=False
    )

    objects = SessionManager()

    def __str__(self):
        return f'Session for user {self.user}'


from sage_session.db import UserSessionStore
