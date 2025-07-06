# Heroku Deployment Guide

This guide will help you deploy your Travel Guide App to Heroku's free tier.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure git is installed and configured

## Quick Deployment (Automated)

1. **Run the deployment script**:
   ```bash
   ./deploy_to_heroku.sh
   ```

2. **Follow the prompts**:
   - Enter your Heroku app name (or let Heroku generate one)
   - Choose whether to create a superuser

## Manual Deployment

### Step 1: Install Heroku CLI and Login

```bash
# Install Heroku CLI (if not already installed)
# macOS: brew install heroku/brew/heroku
# Windows: Download from heroku.com
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login
```

### Step 2: Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### Step 3: Create Heroku App

```bash
# Create app with auto-generated name
heroku create

# OR create app with specific name
heroku create your-app-name
```

### Step 4: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Configure Environment Variables

```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set ALLOWED_HOSTS="localhost,127.0.0.1,your-app-name.herokuapp.com"
```

### Step 6: Deploy the Application

```bash
# Collect static files
cd travelguide
python manage.py collectstatic --noinput
cd ..

# Commit changes
git add .
git commit -m "Prepare for Heroku deployment"

# Deploy to Heroku
git push heroku main
```

### Step 7: Run Database Migrations

```bash
heroku run python manage.py migrate
```

### Step 8: Create Superuser (Optional)

```bash
heroku run python manage.py createsuperuser
```

### Step 9: Open Your App

```bash
heroku open
```

## Important Notes

### Free Tier Limitations

- **Dyno Hours**: 550 hours/month (about 18 hours/day)
- **Database**: 10,000 rows limit with PostgreSQL Mini
- **Sleep Mode**: App sleeps after 30 minutes of inactivity
- **File System**: Ephemeral (files uploaded by users will be lost)

### File Storage

Since Heroku has an ephemeral file system, user-uploaded images will be lost when the dyno restarts. For production, consider:

1. **AWS S3** for file storage
2. **Cloudinary** for image hosting
3. **Google Cloud Storage**

### Environment Variables

Set these in Heroku dashboard or via CLI:

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

### Useful Commands

```bash
# View logs
heroku logs --tail

# Run Django shell
heroku run python manage.py shell

# Create superuser
heroku run python manage.py createsuperuser

# View environment variables
heroku config

# Restart app
heroku restart

# Scale dynos (if needed)
heroku ps:scale web=1
```

## Troubleshooting

### Common Issues

1. **Build Failures**: Check logs with `heroku logs --tail`
2. **Database Issues**: Ensure migrations are run
3. **Static Files**: Verify `collectstatic` was run
4. **Memory Issues**: Consider upgrading dyno size

### Performance Optimization

1. **Enable caching** for better performance
2. **Optimize images** before upload
3. **Use CDN** for static files
4. **Monitor dyno usage** with `heroku ps`

## Security Considerations

1. **Never commit sensitive data** to git
2. **Use environment variables** for secrets
3. **Enable HTTPS** (automatic on Heroku)
4. **Regular security updates**

## Cost Management

- **Free tier**: $0/month (with limitations)
- **Hobby dyno**: $7/month (no sleep mode)
- **Standard dyno**: $25/month (better performance)

Monitor your usage at: https://dashboard.heroku.com/account/billing

## Support

- **Heroku Documentation**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Django on Heroku**: [devcenter.heroku.com/articles/django-app-configuration](https://devcenter.heroku.com/articles/django-app-configuration)
- **Heroku Status**: [status.heroku.com](https://status.heroku.com) 