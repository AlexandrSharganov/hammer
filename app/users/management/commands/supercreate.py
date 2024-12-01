import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from users.models import User



load_dotenv()


class Command(BaseCommand):
    help = "Создаем суперпользователя из .env файла."

    def handle(self, *args, **options):
        phone_number = os.getenv("SUPERUSER_PHONE")
        password = os.getenv("SUPERUSER_PASSWORD")

        if not phone_number or not password:
            self.stdout.write(
                self.style.ERROR(
                    "SUPERUSER_PHONE and SUPERUSER_PASSWORD должен быть установлен в .env"
                )
            )
            return

        if User.objects.filter(phone_number=phone_number).exists():
            self.stdout.write(self.style.ERROR(f"User with phone number '{phone_number}' already exists."))
            return

        User.objects.create_superuser(phone_number=phone_number, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{phone_number}' created successfully."))