#!/bin/bash

# Travel Guide App - Heroku Deployment Script

echo "🚀 Starting Heroku deployment for Travel Guide App..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Heroku deployment"
fi

# Get app name from user
echo "📝 Enter your Heroku app name (or press Enter to let Heroku generate one):"
read app_name

if [ -z "$app_name" ]; then
    echo "🔧 Creating Heroku app with auto-generated name..."
    heroku create
else
    echo "🔧 Creating Heroku app: $app_name"
    heroku create $app_name
fi

# Get the app name from Heroku
APP_NAME=$(heroku apps:info --json | python3 -c "import sys, json; print(json.load(sys.stdin)['app']['name'])")
echo "✅ Heroku app created: $APP_NAME"

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini

# Set environment variables
echo "🔐 Setting environment variables..."
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,$APP_NAME.herokuapp.com"
heroku config:set HEROKU_APP_NAME=$APP_NAME

# Collect static files
echo "📦 Collecting static files..."
cd travelguide
python manage.py collectstatic --noinput
cd ..

# Commit changes
echo "💾 Committing deployment changes..."
git add .
git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Run migrations
echo "🗃️  Running database migrations..."
heroku run python manage.py migrate

# Create superuser (optional)
echo "👤 Would you like to create a superuser? (y/n):"
read create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    heroku run python manage.py createsuperuser
fi

# Open the app
echo "🌐 Opening your app in the browser..."
heroku open

echo "✅ Deployment complete! Your app is live at: https://$APP_NAME.herokuapp.com"
echo ""
echo "📋 Useful commands:"
echo "   heroku logs --tail          # View logs"
echo "   heroku run python manage.py shell  # Django shell"
echo "   heroku run python manage.py createsuperuser  # Create admin user"
echo "   heroku config               # View environment variables" 