from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from notes.models import Note
from notes.serializers import (
    NotesSerializer,
    NoteShareSerializer,
    NoteUpdateSerializer
    )
from notes.permissions import (
    IsOwnerOrSharedUser,
    IsOwner
)
from notes.views import (
    NotesRetrieveUpdateView,
)

User = get_user_model()

class CreateNotesTestCase(TestCase):
    """
        The `test_create_note` function sets up a test environment, creates a user, authenticates the
        client, sends a POST request to create a note, and then asserts various conditions related to
        the created note.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        url = reverse('create-user')
        data = {'title': 'Test Note', 'description': 'This is a test note'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the note is created in the database
        self.assertTrue(Note.objects.filter(title='Test Note').exists())

        # Check if the created note has correct attributes
        created_note = Note.objects.get(title='Test Note')
        self.assertEqual(created_note.title, 'Test Note')
        self.assertEqual(created_note.description, 'This is a test note')
        self.assertEqual(created_note.created_by, self.user)
        self.assertEqual(created_note.updated_by, self.user)

class NoteModelTestCase(TestCase):
    def test_note_model_creation(self):
        """
        The function `test_note_model_creation` creates a test note object and asserts its attributes
        against expected values.
        """
        user = User.objects.create_user(username='testuser', password='password123')
        note = Note.objects.create(title='Test Note', description='This is a test note', created_by=user, updated_by=user)
        
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.description, 'This is a test note')
        self.assertEqual(note.created_by, user)
        self.assertEqual(note.updated_by, user)

class NotesSerializerTestCase(TestCase):
    """
        The below functions test the validity of a serializer for creating notes with valid and invalid
        data.
    """
    def test_serializer_valid_data(self):
        user = User.objects.create_user(username='testuser', password='password123')
        data = {'title': 'Test Note', 'description': 'This is a test note', 'created_by': user.id, 'updated_by': user.id}
        serializer = NotesSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        data = {'title': '', 'description': ''}
        serializer = NotesSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class NoteShareViewTestCase(TestCase):
    """
        The below code defines test cases for sharing a note with a user in the current application.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_share_note(self):
        # Create a note to share
        note = Note.objects.create(title='Test Note', description='This is a test note', created_by=self.user, updated_by=self.user)

        # Prepare data for sharing the note
        data = {'note_id': note.id, 'users': [self.user.id]}  # Share with the same user for testing

        url = reverse('note-share')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the note is shared with the specified user
        note.refresh_from_db()  # Refresh the note object from the database
        self.assertTrue(note.accessible_users.filter(pk=self.user.id).exists())

    def test_share_note_invalid_data(self):
        # Prepare invalid data for sharing the note (missing note_id)
        data = {'users': [self.user.id]}

        url = reverse('note-share')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NoteShareSerializerTestCase(TestCase):
    """
        The below code contains two test functions for testing the validity of a NoteShareSerializer
        with valid and invalid data.
    """
    def test_serializer_valid_data(self):
        user = User.objects.create_user(username='testuser', password='password123')
        note_id = 1  # Provide a valid note ID
        data = {'note_id': note_id, 'users': [user.id]}
        serializer = NoteShareSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        data = {'users': [1]}  # Missing note_id
        serializer = NoteShareSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class NotesRetrieveUpdateViewTestCase(TestCase):
    """
        The below code contains test cases for retrieving and updating notes with authentication and permission checks.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.note = Note.objects.create(title='Test Note', description='This is a test note', created_by=self.user, updated_by=self.user)
        self.view = NotesRetrieveUpdateView.as_view()
        
    def test_retrieve_note(self):
        url = f'/notes/{self.note.id}/'
        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note(self):
        url = f'/notes/{self.note.id}/'
        data = {'title': 'Updated Test Note', 'description': 'This is an updated test note'}
        request = self.factory.put(url, data)
        force_authenticate(request, user=self.user)
        response = self.view(request, id=self.note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_note_invalid_permission(self):
        # Check if user with the same email already exists, if so, delete it
        email = 'anotheruser@example.com'
        try:
            existing_user = User.objects.get(email=email)
            existing_user.delete()
        except User.DoesNotExist:
            pass

        # Create a new user with a unique email address
        another_user = User.objects.create_user(username='anotheruser123', password='password123', email=email)

        url = f'/notes/{self.note.id}/'
        data = {'title': 'Updated Test Note', 'description': 'This is an updated test note'}
        request = self.factory.put(url, data)
        force_authenticate(request, user=another_user)
        response = self.view(request, id=self.note.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class IsOwnerOrSharedUserPermissionTestCase(TestCase):
    '''
        The code below test the functionality for custom permissions
    '''
    def setUp(self):
        email = 'anotheruser@example.com'
        try:
            existing_user = User.objects.get(email=email)
            existing_user.delete()
        except User.DoesNotExist:
            pass
        self.user = User.objects.create_user(username='anotheruser123', password='password123', email=email)
        self.note = Note.objects.create(title='Test Note', description='This is a test note', created_by=self.user, updated_by=self.user)
        self.permission = IsOwnerOrSharedUser()

    def test_has_object_permission_owner(self):
        request = APIRequestFactory().get('/')
        request.user = self.user
        self.assertTrue(self.permission.has_object_permission(request, None, self.note))

    def test_has_object_permission_shared_user(self):
        # Create another user and share the note
        shared_user = User.objects.create_user(username='shareduser', password='password123')
        self.note.accessible_users.add(shared_user)
        request = APIRequestFactory().get('/')
        request.user = shared_user
        self.assertTrue(self.permission.has_object_permission(request, None, self.note))

    def test_has_object_permission_not_owner_nor_shared_user(self):
        # Create another user who is not the owner or shared user of the note
        another_user = User.objects.create_user(username='anotheruser', password='password123')
        request = APIRequestFactory().get('/')
        request.user = another_user
        self.assertFalse(self.permission.has_object_permission(request, None, self.note))

class NotesSerializerTestCase(TestCase):
    def test_serializer_valid_data(self):
        user = User.objects.create_user(username='testuser', password='password123')
        note = Note.objects.create(title='Test Note', description='This is a test note', created_by=user, updated_by=user)
        data = {'title': 'Updated Test Note', 'description': 'This is an updated test note'}
        serializer = NotesSerializer(instance=note, data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        data = {'title': '', 'description': ''}
        serializer = NotesSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class NoteUpdateSerializerTestCase(TestCase):
    def test_serializer_valid_data(self):
        data = {'title': 'Updated Test Note', 'description': 'This is an updated test note'}
        serializer = NoteUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        data = {'title': '', 'description': ''}
        serializer = NoteUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())