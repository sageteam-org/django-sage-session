# Django Sage Session

## What is django-sage-session package?

django-sage-session is a useful package for per user session & private session in Django Web Framework

##### The Latest version of [django-sage-session](https://django-sage-session.readthedocs.io/) documentation

![SageTeam](https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/tag_sage.png?raw=true "SageTeam")

![PyPI release](https://img.shields.io/pypi/v/django-sage-session "django-sage-session")
![Supported Python versions](https://img.shields.io/pypi/pyversions/django-sage-session "django-sage-session")
![Supported Django versions](https://img.shields.io/pypi/djversions/django-sage-session "django-sage-session")
![Documentation](https://img.shields.io/readthedocs/django-sage-session "django-sage-session")

- [Project Detail](#project-detail)
- [Git Rules](#git-rules)
- [Get Started](#get-started)
- [Usage](#usage)
- [Settings](#settings)
- [Admin](#admin)
## Project Detail

- Language: Python > 3.5
- Framework: Django > 3.1

## Git Rules

S.A.G.E. team Git Rules Policy is available here:

- [S.A.G.E. Git Policy](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

## Get Started

First install the package using pip:

```shell
$ pip install django-sage-session
```

Then add sage_cache to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'sage_session',
    ...
]
```

## Usage

For using per user session you have to modify `MIDDLEWARE` in setting:

Replace django Session middleware with sage_session User Session middleware

```python
MIDDLEWARE = [
    ...
    'django.middleware.security.SecurityMiddleware',
    'sage_session.middlewares.UserSessionMiddleware', # provided middleware for per user session
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

For activating Privacy session add it to `MIDDLEWARE`:

Add after UserSessionMiddleware

```python
MIDDLEWARE = [
    ...
    'sage_session.middlewares.UserSessionMiddleware',  # user session
    'sage_session.middlewares.UserSessionPrivacyMiddleware',  # privacy session
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

## Settings
```python
PRIVACYSESSIONS_AUTHED_ONLY = False  # authentication required 
PRIVACYSESSIONS_PRIVACY_IP = True  # validate IP
PRIVACYSESSIONS_PRIVACY_UA = True  # validate user agent
PRIVACYSESSIONS_REMOTE_ADDR_KEY = 'REMOTE_ADDR'  # remote addr key in request (not recommended to change)
PRIVACYSESSIONS_REDIRECT_VIEW = None  # redirect view after logging out
PRIVACYSESSIONS_FAILURE_STATUS = 400 # if not PRIVACYSESSIONS_REDIRECT_VIEW set return status code
PRIVACYSESSIONS_IPV4_LENGTH = 32  # length of ipv4 (not recommended to change)
PRIVACYSESSIONS_IPV6_LENGTH = 64  # length of ipv6 (not recommended to change)
PRIVACYSESSIONS_IP_KEY = '_privacysessions_ip'  # ip key in session
PRIVACYSESSIONS_UA_KEY = '_privacysessions_ua'  # user agent key in session
```

## Admin

`sage_session` also has an admin panel for User Session monitoring, It will activate when you add `sage_session` to `INSTALLED_APPS`
## Team
| [<img src="https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/sepehr.jpeg?raw=true" width="230px" height="230px" alt="Sepehr Akbarzadeh">](https://github.com/sepehr-akbarzadeh) | [<img src="https://github.com/sageteam-org/django-sage-painless/blob/develop/docs/images/mehran.png?raw=true" width="225px" height="340px" alt="Mehran Rahmanzadeh">](https://github.com/mrhnz) |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Sepehr Akbarazadeh Maintainer](https://github.com/sepehr-akbarzadeh)                                                                                                             | [Mehran Rahmanzadeh Maintainer](https://github.com/mrhnz)                                                                                                       |
