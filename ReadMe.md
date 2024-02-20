# How to run
## Requirements : 
- `Python must be installed of version >= 3.9.6`

## Steps : 
- `install all the requirement for requirements.txt`
- `To install requirements run - pip3 install -r requirements.txt`
- `run -> python3 manage.py makemigrations`
- `run -> python3 manage.py migrate`
- `run : python3 manage.py create_default_users`
- `run : python3 manage.py create_random_users`
- `run : python3 manage.py create_dummy_notes`
- `For Local testing/development : python3 manage.py runserver`

## Alternative Step : 
- `run - sh start.sh`

# Django User API

## Model: User

The `User` model represents the user accounts in the application.

### Fields:

- `first_name`: First name of the user (max length: 30 characters).
- `last_name`: Last name of the user (max length: 150 characters).
- `email`: Email address of the user (unique).
- `username`: Username of the user (unique).
- `is_active`: Boolean field indicating whether the user account is active (default: True).
- `is_staff`: Boolean field indicating whether the user is a staff member (default: False).

### Methods:

- `__str__()`: Returns a string representation of the user, including email and username.

## View: UserCreateAPIView

The `UserCreateAPIView` is responsible for handling user creation requests.

### Endpoint:

- `POST /signup/`: Creates a new user account.

### Permissions:

- `AllowAny`: Allows access to any user, even if they are not authenticated.

### Serializer:

- `CustomUserSerializer`: Serializer class used for user creation.

#### Additional Logic:

- Checks if the provided email or username is already in use before creating a new user account.

## URLs

### User Creation and Authentication Endpoints:

- `POST /signup/`: Create a new user account.
- `POST /token/`: Obtain a JSON Web Token (JWT) pair for authentication.
- `POST /token/refresh/`: Refresh an existing JWT pair.

These endpoints are used for user registration, authentication, and token management.

# Django Notes API

## Model: Note

The `Note` model represents the notes in the application.

### Fields:

- `title`: Title of the note (max length: 255 characters).
- `description`: Description or content of the note.
- `accessible_users`: Many-to-many relationship with the `User` model, representing users who have access to the note.

### Additional Features:

- Inherits from `TimestampedModel` for automatic timestamp fields (`created_at` and `updated_at`).
- Inherits from `UserStampedModel` for fields related to user creation and updating.
- Tracks changes made to the note using the `FieldTracker` utility.
- Provides a custom `save()` method to track changes and create history objects.
- Uses the `History` model to store historical data for changes made to notes.

## Model: History

The `History` model is related to storing historical data for changes made to notes.

### Fields:

- `updated_by`: ForeignKey to the `User` model, representing the user who made the update.
- `old_value`: Text field containing the previous value of the note.
- `new_value`: Text field containing the updated value of the note.
- `activity`: Text field representing the activity or action performed on the note.
- `note`: ForeignKey to the `Note` model, establishing a relationship between the history entry and the corresponding note.


### Methods:

- `__str__()`: Returns a string representation of the note, including its title and primary key.

## View: NotesRetrieveUpdateView

The `NotesRetrieveUpdateView` is responsible for retrieving and updating notes.

### Endpoints:

- `GET /<id>/`: Retrieve a specific note.
- `PUT /<id>/`: Update a specific note.
- `DELETE /<id>/`: Delete a specific note.

### Permissions:

- `IsAuthenticated`: Allows access only to authenticated users.
- `IsOwnerOrSharedUser`: Allows access to the owner of the note or users with shared access.

### Serializer:

- `NotesSerializer`: Serializer class used for note serialization.

## URLs

### Note Endpoints:

- `POST notes/create/`: Create a new note.
- `GET,PUT,DELETE notes/<id>/`: Retrieve, updated or delete a specific note.
- `POST notes/share/`: Share a note with other users.
- `GET notes/version-history/<id>/`: Retrieve the version history of a note.

## Permissions

### IsOwnerOrSharedUser

This permission class checks if the requesting user has permission to access a note based on ownership or accessibility.

### IsOwner

This custom permission class checks if the user is the owner of a specific note.

## management commands

### create_default_users
-`This commands create two users with admin permissions username = admin and system`
-`These users have access to all the pre built notes in the system`

### create_random_users
-`This management commands create 10 users for testing purpose where all the users shares the same password`

### create_dummy_notes
-`This management commands create 10 notes for testing purpose and the users admin and system have the access to all the prebuilt notes.`