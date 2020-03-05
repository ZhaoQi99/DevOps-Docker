#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

ENV = os.environ.get('ENV')


def main():
    if ENV is None:
        raise EnvironmentError(
            "Couldn't get 'ENV' environment variable.Are you sure"
            "you have set it in your command or system."
            "Please set it and then run your command as like this:"
            "ENV=dev python manage.py command"
        )
    if ENV in ['dev', 'test', 'pro']:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qops_server.settings.' + ENV)
    else:
        raise EnvironmentError(
            "You have used an invalid ENV variable!"
            "ENV environment variable must be in ['dev', 'test', 'pro']"
        )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
