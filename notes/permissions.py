from rest_framework import permissions

class IsOwnerOrSharedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        """
        The function checks if the requesting user has permission to access an object based on ownership
        or accessibility.
        
        :return: The `has_object_permission` method is returning a boolean value based on whether the
        requesting user is the owner of the object (`obj`) or is in the list of accessible users for
        that object. If the requesting user is the owner or in the list of accessible users, it returns
        `True`, otherwise it returns `False`.
        """
        # Check if the requesting user is the owner of the note
        if request.user == obj.created_by:
            return True
        # Check if the requesting user is in the list of accessible users
        elif request.user in obj.accessible_users.all():
            return True
        return False

class IsOwner(permissions.BasePermission):
    '''
        This is a custom permission class which checks if the 
        user is allowed to access a particular note or not
    '''

    def has_object_permission(self, request, view, obj) -> bool:
        # Check if the requesting user is the owner of the note
        return request.user == obj.created_by