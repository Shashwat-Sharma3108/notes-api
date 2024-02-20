from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create system and admin users with password Test@1234'

    def handle(self, *args, **kwargs):
        for username in ["system", "admin"]:
            email = f"{username}@example.com"
            password = "Test@1234"

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name="Dummy",
                last_name="User",
                is_staff = True,
                is_superuser = True
            )


        self.stdout.write(self.style.SUCCESS('Successfully created dummy users.'))