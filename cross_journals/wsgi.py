"""
Release: 0.1
Author: Golikov Ivan
Date: 10.07.2017

WSGI config for cross_journals project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cross_journals.settings")

application = get_wsgi_application()
