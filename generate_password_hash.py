import os
import django
from django.conf import settings

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRIS.settings')
django.setup()

from django.contrib.auth.hashers import make_password

# Generate a proper Django password hash
test_password = "Pass@123"  # This will be the actual password users can login with
hashed_password = make_password(test_password)
print(f"\nPassword: {test_password}")
print(f"Hashed value to use in fixture: {hashed_password}")