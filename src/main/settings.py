"""
Django settings for mud-server project.

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Set base directory as parent's folder (src)
BASE_DIR = os.path.dirname(BASE_DIR)

ALLOWED_HOSTS = ['']

# [production adjustment] The secret key should be passed by env vars and be kept in secret.
# The reason is that Django uses to for generating hashes.
# User passwords and sessions would be compromised if the secret key was disclosed
# https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key
SECRET_KEY = 'h7@sk*^1n#o%wre1ck&49kio89mfgzwt@68in8-(j5)+mpouv_'

DEBUG = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'channels',
    'contrib.mud_auth',
    'world'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# [production adjustment] The database should a production-suitable RDBMS like PostgreSQL and their credentials
# should be passed by env vars.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom User Model
AUTH_USER_MODEL = 'mud_auth.User'

ASGI_APPLICATION = "main.asgi.application"

# [production adjustment] Django channels recommends and supports Redis as backend for channel layers for production use
# (https://channels.readthedocs.io/en/stable/topics/channel_layers.html#redis-channel-layer)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Basic commands of this MUD game
MUD_COMMANDS_BASE = {
    'server.commands.login.CommandLogin': 'server.commands.parsers.parser_login.CommandParserLogin',
    'server.commands.register.CommandRegister': 'server.commands.parsers.parser_register.CommandParserRegister',
    'server.commands.logout.CommandLogout': 'server.commands.parsers.parser_logout.CommandParserLogout',
    'server.commands.help.CommandHelp': 'server.commands.parsers.parser_help.CommandParserHelp',
    'server.commands.say.CommandSay': 'server.commands.parsers.parser_say.CommandParserSay',
    'server.commands.move.north.CommandNorth': 'server.commands.parsers.parser_move.CommandParserMove',
    'server.commands.move.south.CommandSouth': 'server.commands.parsers.parser_move.CommandParserMove',
    'server.commands.move.west.CommandWest': 'server.commands.parsers.parser_move.CommandParserMove',
    'server.commands.move.east.CommandEast': 'server.commands.parsers.parser_move.CommandParserMove',
    'server.commands.look.look.CommandLook': 'server.commands.parsers.parser_look.CommandParserLook',
}
