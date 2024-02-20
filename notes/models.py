from django.db import models
from django.contrib.auth import get_user_model
from model_utils import FieldTracker
from django.db import transaction


class TimestampedModel(models.Model):
    '''
        Abstract model for adding datetimmefields.
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    '''
        Abstract model for adding User model related fields
    '''
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='%(class)s_created', null=True)
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='%(class)s_updated', null=True)

    class Meta:
        abstract = True


class Note(TimestampedModel, UserStampedModel):
    '''
        This class inherits from 
            - TimestampedModel for adding fields like : created_at and updated_at
            - UserStampedModel for adding fields like : created_by and updated_by
    '''
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    accessible_users = models.ManyToManyField(get_user_model(), related_name='accessible_notes')

    #For tracking changes in models
    tracker = FieldTracker()

    def __str__(self):
        return f"{self.title} {self.pk}"

    def save(self, *args, **kwargs):
        '''
            Custom save method for tracking changes at model level
        '''
        if self.pk:
            changed_fields = self.tracker.changed()
            for field, original_value in changed_fields.items():
                if field == "updated_by_id":
                    continue
                new_value = getattr(self, field)
                # Log the change
                self.track_changes(field, original_value, new_value)
        super(Note, self).save(*args, **kwargs)
    
    @transaction.atomic
    def track_changes(self, field, old_value, new_value):
        '''
            Function to create History object which tracks the 
            changes made to a particular note.
        '''
        try:
            user = self.updated_by
            History.objects.create(
                updated_by = user,
                note = self,
                old_value = old_value,
                new_value = new_value,
                activity = f"{user} updated {field} from {old_value} to {new_value}"
            )
        except Exception as e:
            print(f"ERROR : {e}")

class History(TimestampedModel):    
    '''
        This class inherits from a `TimestampedModel` class and is related to storing historical
        data.
    '''
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='%(class)s_updated', null=True)
    old_value = models.TextField()
    new_value = models.TextField()
    activity =  models.TextField(default='')
    note = models.ForeignKey(Note, blank=False, null=True, on_delete=models.CASCADE,)