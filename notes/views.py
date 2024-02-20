from rest_framework.generics import (
    CreateAPIView, 
    GenericAPIView,
    RetrieveAPIView,
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from django.shortcuts import get_object_or_404

from notes.serializers import (
    NotesSerializer,
    HistorySerializer,
    NoteShareSerializer,
    NoteUpdateSerializer
    )
from notes.models import (
    Note,
    History
    )
from notes.permissions import (
    IsOwnerOrSharedUser,
    IsOwner
    )

class CreateNotes(CreateAPIView):
    '''
        View for creating notes
    '''
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user, updated_by=self.request.user)

class NoteShareView(CreateAPIView):
    '''
        View for Sharing notes
    '''
    serializer_class = NoteShareSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note_id = serializer.validated_data['note_id']
        users = serializer.validated_data['users']

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response({"message": "Note does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Share the note with the specified users
        note.accessible_users.add(*users)

        return Response({"message": "Note shared successfully"}, status=status.HTTP_200_OK)

class NotesRetrieveUpdateView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):
    '''
        View for updating ,reading and deleting a particular note
        based on the provided permissions
    '''
    queryset = Note.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSharedUser]
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NoteUpdateSerializer
        return self.serializer_class

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user in self.get_object().accessible_users.all():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"error" : "You do not have the permission to perform this action."},
                status = status.HTTP_403_FORBIDDEN
                )

class NoteVersionHistoryView(RetrieveAPIView):
    '''
        View for fetching the history changes of a particular note
        There are permissions applied here for checking if the
        logged in user can access the note or not
    '''
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSharedUser]

    def retrieve(self, request, id):
        note = get_object_or_404(Note, id=id)
        history_entries = History.objects.filter(note=note)
        serializer = self.get_serializer(history_entries, many=True)
        return Response(serializer.data)