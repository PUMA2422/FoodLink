import os
from django.core.management.commands.runserver import Command as RunserverCommand
from django.conf import settings
import mysql.connector
from mysql.connector import errorcode

class Command(RunserverCommand):
    def handle(self, *args, **options):

        # Check if this is the main process (not the autoreloader process)
        if os.environ.get('RUN_MAIN') != 'true':
            pass
        else:
            # Only run the MySQL prompt and configuration in the main process
            if not hasattr(settings, 'MYSQL_CONFIGURED') or not settings.MYSQL_CONFIGURED:
                mysql_config = self.get_mysql_config()
                self.ensure_database_exists(mysql_config)

                # Update settings with MySQL configuration
                settings.DATABASES['default'].update(mysql_config)

                # Set MYSQL_CONFIGURED to True after the prompt
                settings.MYSQL_CONFIGURED = True

        super().handle(*args, **options)

    def get_mysql_config(self):
        # Prompt for MySQL configuration
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
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
        }

    def ensure_database_exists(self, config):
        # Connect to MySQL server (without specifying the database)
        try:
            connection = mysql.connector.connect(
                host=config['HOST'],
                port=config['PORT'],
                user=config['USER'],
                password=config['PASSWORD']
            )
            cursor = connection.cursor()

            # Check if the database exists, and if not, create it
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['NAME']} DEFAULT CHARACTER SET 'utf8'")
            print(f"Database '{config['NAME']}' ensured or created successfully.")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your MySQL username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist, and an error occurred while creating it.")
            else:
                print(err)
