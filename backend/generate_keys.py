#!/usr/bin/env python
import secrets
import string

def generate_secret_key(length=50):
    """Generate a random secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("=== Django Secret Keys ===")
    print()
    
    # Generate Django SECRET_KEY
    django_secret = generate_secret_key(50)
    print(f"SECRET_KEY={django_secret}")
    print()
    
    # Generate JWT secret (can be same or different)
    jwt_secret = generate_secret_key(50)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print()
    
    print("=== Copy these to your .env file ===")
    print("Note: Keep these secret and never commit them to version control!") 