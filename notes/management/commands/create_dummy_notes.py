import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notes.models import Note

class Command(BaseCommand):
    help = 'Initialize the Note model with random data for title and description'

    def handle(self, *args, **kwargs):
        '''
            This is a management command used to create dummy data in system,
            Also this function gives access of all the notes to System and 
            Admin user.
        '''
        User = get_user_model()
        users = User.objects.all().exclude(username__in=("system","admin"))
        system_user = User.objects.get(username="system")
        admin_user = User.objects.get(username="admin")
        # Create a new note for each user with random title and description
        for user in users:
            title = ''.join(random.choices(string.ascii_letters, k=10))  # Generate random title
            description = ''.join(random.choices(string.ascii_letters, k=50))  # Generate random description

            note = Note.objects.create(
                title=title,
                description=description,
                created_by=user,
                updated_by=user
            )
            
            note.accessible_users.set([system_user, admin_user])  # Clear the accessible_users set

        self.stdout.write(self.style.SUCCESS('Successfully initialized notes with random data for title and description.'))