from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from ... import settings


class Command(BaseCommand):
    args = ""
    help = "Tests all apps in the MY_APPS list in the settings file"

    def handle(self, *args, **kwargs):
        call_command("test", *settings.MY_APPS)
