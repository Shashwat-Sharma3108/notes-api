from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from notes.models import Note, History


class NotesSerializer(ModelSerializer):
    '''
        ModelSerializer for updating and creating Notes.
    '''
    class Meta:
        model = Note
        fields = ("title","description")

class HistorySerializer(ModelSerializer):
    '''
        ModelSerializer for sending data from History.
    '''
    class Meta:
        model = History
        fields = ('updated_by', 'old_value', 'new_value', 'activity', 'note')

class NoteShareSerializer(serializers.Serializer):
    '''
        Serializer for validating the input data while updating the
        permissions for a particular note.

        It checks if the list of user ids provided belongs to an
        exisisting user in our system or not.
    '''
    note_id = serializers.IntegerField()
    users = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True)

class NoteUpdateSerializer(serializers.ModelSerializer):
    '''
        ModelSerializer for validating the data while updating a particular
        note.
    '''
    class Meta:
        model = Note
        fields = ['description']