import logging

from django.contrib import auth
from django.contrib.sessions.backends.base import CreateError, SessionBase
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError, router, transaction
from django.utils import timezone
from django.utils.encoding import force_text


class UserSessionStore(SessionStore):
    """Implements database session store."""

    def __init__(
            self,
            session_key=None,
            user_agent=None,
            ip=None,
            location=None,
            device_brand=None,
            device_model=None,
            browser=None,
            browser_version=None,
            os=None,
            os_version=None,
            is_mobile=False,
            is_tablet=False,
            is_touch_capable=False,
            is_pc=False,
            is_bot=False
    ):
        super(UserSessionStore, self).__init__(session_key)
        # Truncate user_agent string to max_length of the CharField
        self.user_agent = user_agent[:200] if user_agent else user_agent
        self.ip = ip
        self.location = location
        self.device_model = device_model
        self.device_brand = device_brand
        self.browser = browser
        self.browser_version = browser_version
        self.os = os
        self.os_version = os_version
        self.is_mobile = is_mobile
        self.is_tablet = is_tablet
        self.is_touch_capable = is_touch_capable
        self.is_pc = is_pc
        self.is_bot = is_bot
        self.user_id = None

    def __setitem__(self, key, value):
        if key == auth.SESSION_KEY:
            self.user_id = value
        super(UserSessionStore, self).__setitem__(key, value)

    def load(self):
        try:
            s = Session.objects.get(
                session_key=self.session_key,
                expire_date__gt=timezone.now()
            )
            self.user_id = s.user_id
            return self.decode(s.session_data)
        except (Session.DoesNotExist, SuspiciousOperation) as e:
            if isinstance(e, SuspiciousOperation):
                logger = logging.getLogger(
                    'django.security.%s' % e.__class__.__name__
                )
                logger.warning(force_text(e))
            return {}

    def save(self, must_create=False):
        """Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        if self.session_key is None:
            return self.create()
        data = self._get_session(no_load=must_create)
        obj = Session(
            session_key=self._get_or_create_session_key(),
            session_data=self.encode(data),
            expire_date=self.get_expiry_date(),
            user_agent=self.user_agent,
            user_id=self.user_id,
            ip=self.ip,
            location=self.location,
            device_brand=self.device_brand,
            device_model=self.device_model,
            browser=self.browser,
            browser_version=self.browser_version,
            os=self.os,
            os_version=self.os_version,
            is_mobile=self.is_mobile,
            is_tablet=self.is_tablet,
            is_touch_capable=self.is_touch_capable,
            is_pc=self.is_pc,
            is_bot=self.is_bot
        )
        using = router.db_for_write(Session, instance=obj)
        try:
            with transaction.atomic(using):
                self.delete_duplicate()
                obj.save(force_insert=must_create, using=using)
        except IntegrityError as e:
            if must_create and 'session_key' in str(e):
                raise CreateError
            raise

    def delete_duplicate(self):
        """delete other session objects for user"""
        return Session.objects.filter(user_id=self.user_id).delete()

    def clear(self):
        """clear session"""
        super(UserSessionStore, self).clear()
        self.user_id = None


from user_session.models import Session
