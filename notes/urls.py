from django.urls.conf import path
from notes.views import (
    CreateNotes,
    NotesRetrieveUpdateView,
    NoteShareView,
    NoteVersionHistoryView
    )


urlpatterns = [
    path("create/", CreateNotes.as_view(), name='create-user'),
    path("<int:id>/", NotesRetrieveUpdateView.as_view(), name='get-edit-note'),
    path("share/", NoteShareView.as_view(), name='note-share'),
    path("version-history/<int:id>/", NoteVersionHistoryView.as_view(), name='get-history')
]
