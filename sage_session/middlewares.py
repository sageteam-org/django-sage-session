import warnings
import logging

from netaddr import (
    IPNetwork,
    IPAddress,
    AddrConversionError,
    AddrFormatError
)

from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings as dj_settings
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.encoding import force_text

from sage_session.db import UserSessionStore
from sage_session.services import analyse_user_agent, get_ip_location
from sage_session import settings

SESSION_IP_KEY = getattr(settings, 'PRIVACYSESSIONS_IP_KEY', '_privacysessions_ip')
SESSION_UA_KEY = getattr(settings, 'PRIVACYSESSIONS_UA_KEY', '_privacysessions_ua')

logger = logging.getLogger('privacysessions')


class UserSessionMiddleware(SessionMiddleware):
    """A middleware that adds ip and user_agent to the session store."""

    def process_request(self, request):
        session_key = request.COOKIES.get(dj_settings.SESSION_COOKIE_NAME, None)
        ip = request.META.get('REMOTE_ADDR', '')
        try:
            location = get_ip_location(ip)
        except Exception as e:
            warnings.warn(str(e))
            location = None
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        (
            device_brand,
            device_model,
            browser,
            browser_version,
            os,
            os_version,
            is_mobile,
            is_tablet,
            is_touch_capable,
            is_pc,
            is_bot
        ) = analyse_user_agent(user_agent)
        request.session = UserSessionStore(
            ip=ip,
            user_agent=user_agent,
            session_key=session_key,
            location=location,
            device_model=device_model,
            device_brand=device_brand,
            browser=browser,
            browser_version=browser_version,
            os=os,
            os_version=os_version,
            is_mobile=is_mobile,
            is_tablet=is_tablet,
            is_touch_capable=is_touch_capable,
            is_pc=is_pc,
            is_bot=is_bot
        )


class UserSessionPrivacyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Short circuit when request doesn't have session
        if not hasattr(request, 'session'):
            return

        # Short circuit for option to require authed users
        if getattr(settings, 'PRIVACYSESSIONS_AUTHED_ONLY', False):
            user = getattr(request, 'user', None)
            # No logged in user -- ignore checks
            if not user or not hasattr(user, 'is_authenticated') or not user.is_authenticated:
                return

        # Extract remote IP address for validation purposes
        remote_addr_key = getattr(settings, 'PRIVACYSESSIONS_REMOTE_ADDR_KEY', 'REMOTE_ADDR')
        remote_addr = request.META.get(remote_addr_key)
        if remote_addr:
            remote_addr = remote_addr.split(',')[0]

        # Clear the session and handle response when request doesn't validate
        if not self.validate_ip(request, remote_addr) or not self.validate_ua(request):
            if getattr(settings, 'PRIVACYSESSIONS_AUTHED_ONLY', False):
                from django.contrib.auth import logout
                logout(request)
            else:  # logout(...) flushes the session so ensure it only happens once
                request.session.flush()
            logger.warning("Destroyed session due to invalid change of remote host or user agent")
            redirect_view = getattr(settings, 'PRIVACYSESSIONS_REDIRECT_VIEW', None)
            if redirect_view:
                return redirect(reverse(redirect_view))
            else:
                status = getattr(settings, 'PRIVACYSESSIONS_FAILURE_STATUS', 400)
                return HttpResponse(status=status)

        # Set the UA/IP Address on the session since they validated correctly
        request.session[SESSION_IP_KEY] = remote_addr
        if request.META.get('HTTP_USER_AGENT'):
            request.session[SESSION_UA_KEY] = force_text(request.META['HTTP_USER_AGENT'], errors='replace')

    def validate_ip(self, request, remote_ip):
        """check request ip and session stored ip"""
        # When we aren't configured to restrict on IP address
        if not getattr(settings, 'PRIVACYSESSIONS_PRIVACY_IP', True):
            return True
        # When the IP address key hasn't yet been set on the request session
        if SESSION_IP_KEY not in request.session:
            return True
        # When there is no remote IP, check if one has been set on the session
        session_ip = request.session[SESSION_IP_KEY]
        if not remote_ip:
            if session_ip:  # session has remote IP value so validate :-(
                return False
            else:  # Session doesn't have remote IP value so possibly :-)
                return True

        # Compute fuzzy IP compare based on settings on compare sensitivity
        if not session_ip:
            return False
        session_network = IPNetwork(session_ip)
        remote_ip = IPAddress(remote_ip)
        try:
            session_network = session_network.ipv4()
            remote_ip = remote_ip.ipv4()
            session_network.prefixlen = getattr(settings, 'PRIVACYSESSIONS_IPV4_LENGTH', 32)
        except AddrConversionError:
            try:
                session_network.prefixlen = getattr(settings, 'PRIVACYSESSIONS_IPV6_LENGTH', 64)
            except AddrFormatError:
                # session_network must be IPv4, but remote_ip is IPv6
                return False
        return remote_ip in session_network

    def validate_ua(self, request):
        """check request user agent and session stored user agent"""
        # When we aren't configured to restrict on user agent
        if not getattr(settings, 'PRIVACYSESSIONS_PRIVACY_UA', True):
            return True
        # When the user agent key hasn't been set yet in the request session
        if SESSION_UA_KEY not in request.session:
            return True
        # Compare the new user agent value with what is known about the session
        return request.session[SESSION_UA_KEY] == force_text(request.META['HTTP_USER_AGENT'], errors='replace')
