#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Make migrations and migrate
python manage.py makemigrations
python manage.py migrate

# Run management commands
python manage.py create_default_users
python manage.py create_random_users
python manage.py create_dummy_notes

# Start the server
python manage.py runserver
