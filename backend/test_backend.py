#!/usr/bin/env python
import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aitodo.settings')
django.setup()

# Test imports
from authentication.models import User
from api.models import Todo

print("✅ Django backend is working!")
print(f"✅ User model: {User}")
print(f"✅ Todo model: {Todo}")
print("✅ All models imported successfully")

# Test database connection
try:
    User.objects.count()
    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database error: {e}") 