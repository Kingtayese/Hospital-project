# King Care Hospital - Render Deployment Guide

This guide will help you deploy the King Care Hospital Management System to Render.

## Prerequisites

1. A GitHub account with this project repository
2. A Render account (sign up at https://render.com)
3. Basic understanding of web deployment

## Deployment Steps

### 1. Push Code to GitHub

Make sure your code is pushed to a GitHub repository.

### 2. Create PostgreSQL Database on Render

1. Log in to your Render dashboard
2. Click "New +" and select "PostgreSQL"
3. Choose a name for your database (e.g., `king-care-hospital-db`)
4. Select your desired plan (Free tier available)
5. Click "Create Database"
6. Note down the database connection details

### 3. Deploy Web Service

1. In Render dashboard, click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure the following settings:

#### Basic Settings:
- **Name**: `king-care-hospital`
- **Environment**: `Python 3`
- **Region**: Choose your preferred region
- **Branch**: `main` (or your default branch)

#### Build & Deploy:
- **Root Directory**: Leave empty (or specify if your Django project is in a subdirectory)
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn king_care_hospital.wsgi:application`

#### Environment Variables:
Add these environment variables in the Render dashboard:

```
DATABASE_URL=<your-postgresql-connection-string>
SECRET_KEY=<generate-a-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-render-app-url>
```

### 4. Environment Variables Details

#### DATABASE_URL
- Get this from your PostgreSQL database on Render
- Format: `postgresql://username:password@host:port/database_name`
- Example: `postgresql://user:pass@render-host.com:5432/mydb`

#### SECRET_KEY
- Generate a new Django secret key
- You can use Django's built-in generator or online tools
- Keep this secure and never share it publicly

#### DEBUG
- Set to `False` for production
- This disables debug mode and enables production optimizations

#### ALLOWED_HOSTS
- Your Render app URL (e.g., `your-app-name.onrender.com`)
- You can add multiple hosts separated by commas

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Wait for the build to complete (this may take a few minutes)
4. Once deployed, you'll get a URL to access your application

## Post-Deployment Steps

### 1. Create Superuser

After successful deployment, create an admin user:

1. Go to your Render service dashboard
2. Click on "Shell" tab
3. Run: `python manage.py createsuperuser`
4. Follow the prompts to create your admin account

### 2. Test Your Application

1. Visit your Render app URL
2. Test the main functionality:
   - User registration and login
   - Patient management
   - Appointment scheduling
   - Admin panel access

### 3. Configure Email Settings (Optional)

Update email settings in `settings.py` if you want to use a different email service:

```python
EMAIL_HOST = 'your-smtp-host'
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the build logs in Render dashboard
2. **Static Files Not Loading**: Ensure `collectstatic` runs in build script
3. **Database Connection Issues**: Verify DATABASE_URL is correct
4. **Permission Errors**: Make sure `build.sh` is executable

### Useful Commands:

```bash
# Check Django configuration
python manage.py check

# Verify database connection
python manage.py dbshell

# Collect static files manually
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
```

## Security Considerations

1. **Never commit secrets** to version control
2. **Use environment variables** for all sensitive data
3. **Keep DEBUG=False** in production
4. **Regularly update dependencies** for security patches
5. **Use HTTPS** (Render provides this automatically)

## Support

If you encounter issues during deployment:

1. Check Render's deployment logs
2. Verify all environment variables are set correctly
3. Ensure your database is properly configured
4. Review Django's deployment checklist

## Features Available After Deployment

Your deployed King Care Hospital Management System includes:

- **Multi-user Dashboard**: Admin, Doctor, Patient, Pharmacist, Laboratory, Accountant, Receptionist
- **Patient Management**: Registration, medical history, appointments
- **Appointment System**: Scheduling with doctor availability
- **Pharmacy Management**: Medicine inventory, sales tracking
- **Laboratory**: Blood bank, donor management
- **Accounting**: Invoice generation, payment tracking
- **Email Notifications**: Patient registration confirmations
- **Responsive Design**: Works on desktop and mobile devices

## Maintenance

- **Regular Backups**: Render provides automatic database backups
- **Monitor Logs**: Check application logs regularly
- **Update Dependencies**: Keep packages updated for security
- **Database Maintenance**: Monitor database performance and storage