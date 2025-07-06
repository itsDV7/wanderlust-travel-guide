#!/usr/bin/env python3
"""
Setup script for Wanderlust Travel Guide App
This script helps configure the project for first-time setup.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def setup_environment():
    """Set up the environment configuration."""
    print("🚀 Setting up Wanderlust Travel Guide App...")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping environment setup.")
        return
    
    # Copy env.example to .env
    if os.path.exists('env.example'):
        with open('env.example', 'r') as example_file:
            env_content = example_file.read()
        
        # Generate a new secret key
        new_secret_key = generate_secret_key()
        env_content = env_content.replace('your_django_secret_key_here', new_secret_key)
        
        # Write the new .env file
        with open('.env', 'w') as env_file:
            env_file.write(env_content)
        
        print("✅ Created .env file with a new SECRET_KEY")
        print("📝 Please edit .env file to add your Google Places API key and other settings")
    else:
        print("❌ env.example file not found. Please create it manually.")

def main():
    """Main setup function."""
    print("🧭 Wanderlust Travel Guide App Setup")
    print("=" * 40)
    
    setup_environment()
    
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run database migrations: python manage.py migrate")
    print("3. Create a superuser: python manage.py createsuperuser")
    print("4. Start the server: python manage.py runserver")
    print("\n🔒 Security reminder: Never commit .env files to version control!")

if __name__ == "__main__":
    main() 