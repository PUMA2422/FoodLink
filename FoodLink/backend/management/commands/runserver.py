from django.core.management.commands.runserver import Command as RunserverCommand
from django.conf import settings

class Command(RunserverCommand):
    def get_mysql_config(self):
        print("Please provide MySQL server details:")
        host = input("Enter MySQL host (default 'localhost'): ") or 'localhost'
        port = input("Enter MySQL port (default 3306): ") or '3306'
        user = input("Enter MySQL username: ")
        password = input("Enter MySQL password: ")
        db_name = "FoodLink"

        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }

    def handle(self, *args, **options):
        # Prompt for MySQL details
        mysql_config = self.get_mysql_config()

        # Update Django settings dynamically
        settings.DATABASES['default'] = mysql_config

        # Continue with the usual runserver logic
        super().handle(*args, **options)
