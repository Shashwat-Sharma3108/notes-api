from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    help = 'Create dummy users with password Test@1234'

    def handle(self, *args, **kwargs):
        for _ in range(10):  # Create 10 dummy users
            username = get_random_string(length=10)
            email = f"{username}@example.com"
            password = "Test@1234"

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name="Dummy",
                last_name="User",
            )

        self.stdout.write(self.style.SUCCESS('Successfully created dummy users.'))
