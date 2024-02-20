from django.contrib import admin
from notes.models import (
    History, 
    Note,
    )

# Register your models here.
admin.site.register(History)
admin.site.register(Note)