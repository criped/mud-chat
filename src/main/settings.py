"""
Django settings for mud-server project.

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Set base directory as parent's folder (src)
BASE_DIR = os.path.dirname(BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h7@sk*^1n#o%wre1ck&49kio89mfgzwt@68in8-(j5)+mpouv_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


if DEBUG is True:
    DATABASE_CONF_DEFAULT = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
else:
    DATABASE_CONF_DEFAULT = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASENAME', ''),
        'USER': os.environ.get('DATABASEUSER', ''),
        'PASSWORD': os.environ.get('DATABASEPASSWORD', ''),
        'HOST': os.environ.get('DATABASEHOST', ''),
        'PORT': os.environ.get('DATABASEPORT', ''),
    }


DATABASES = {
    'default': DATABASE_CONF_DEFAULT
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

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

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
