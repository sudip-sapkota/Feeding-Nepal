from pathlib import Path
import os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-15o8=z)i5^)g+h^-0)9$-a96fi(d6##@7bwy^cw+hxk0jb-g1$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Change to appropriate domain or IP addresses in production

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your custom apps
    'donor',  # Ensure your custom app is listed here
    'volunteer',
    'adminpanel',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FeedingNepal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Global templates directory
            BASE_DIR / 'donor' / 'templates',  # Template folder for 'donor' app
        ],
        'APP_DIRS': True,  # Allow template search in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # for message
                'volunteer.context_processors.volunteer_context', #for load the context

            ],
        },
    },
]

WSGI_APPLICATION = 'FeedingNepal.wsgi.application'

# Database configuration (Ensure this is correct for your local setup)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'feed',  # Ensure this matches the name of your database
        'USER': 'root',  # Ensure the correct username is provided
        'PASSWORD': 'Root@123',  # Ensure the correct password is provided
        'HOST': 'localhost',  # If MySQL is hosted locally
        'PORT': '3306',  # Default MySQL port
    }
}

# Password validation settings (Default Django validation)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Ensure this is correct
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Required for collectstatic command to gather static files

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enable Django messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'  # Store messages in the session

# Session settings for persistence
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions
SESSION_COOKIE_AGE = 3600  # Session expiry time (1 hour in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Don't expire session on browser close (set to True to expire on close)
SESSION_SAVE_EVERY_REQUEST = True  # Save the session to the database on every request