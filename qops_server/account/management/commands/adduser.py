import getpass
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Create a user.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('-u', metavar='username', help='账户名称')
        parser.add_argument('-p', metavar='password', help='账户密码')

    def handle(self, *args, **options):
        username = options['u']
        password = options['p']
        if username:
            username = self.validate_username(username)
        try:
            while username is None:
                username = self.get_input_data(_('username'))
                username = self.validate_username(username)
            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass('Password (again): ')
                if password != password2:
                    self.stderr.write("Error: Your passwords didn't match.")
                    password, password2 = None, None
                    continue
        except KeyboardInterrupt:
            self.stderr.write('\nOperation cancelled.')
            sys.exit(1)
        UserModel.objects.create_user(username=username, password=password, is_admin=False)
        self.stdout.write(f'Create user {username} successfully!')

    def get_input_data(self, message):
        raw_value = input(message + ': ')
        return raw_value

    def validate_username(self, username):
        if UserModel.objects.filter(username=username):
            self.stdout.write(f'Error: User {username} has exists.')
            return None
        return username
