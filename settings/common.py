# Django settings for osubus_web project.
from django.conf import global_settings

# first, get the project directory
import os.path
project_dir = os.path.split(os.path.abspath(__file__))[0]
project_dir = os.path.split(project_dir)[0]
def project_path(p):
    return os.path.join(project_dir, p)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Aaron Griffith', 'aargri@gmail.com'),
)

MANAGERS = ADMINS

# get rid of pesky slashes on flatpages
#APPEND_SLASH = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = project_path('roots/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = project_path('roots/static')

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# A list of locations of additional static files
STATICFILES_DIRS = (project_path('static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xx%f5usqol%i9pjdx26dn)qh&b_imi5&fx+yd^s1cwary$fa!i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

FILE_UPLOAD_HANDLERS = (
    'uploader.upload_handlers.UploadProgressCachedHandler',
) + global_settings.FILE_UPLOAD_HANDLERS

AUTHENTICATION_BACKENDS = (
    'social_github.backends.github.GitHubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_IMPORT_BACKENDS = (
    'social_github.backends',
)

# URL of the login page.
LOGIN_URL = '/login'
LOGIN_ERROR_URL = '/login-error'
LOGIN_REDIRECT_URL = '/'
GITHUB_OAUTH2_CLIENT_KEY = '7abf70feb670e4e594a6'
GITHUB_OAUTH2_CLIENT_SECRET = 'bead9d1870ef6c963c0256e0b74fdee36d6f746a'
SOCIAL_AUTH_ERROR_KEY = 'social_errors'

# doc build post-hook key
UPDATE_HOOK_KEY = 'a9ffffab42257e86'
UPDATE_HOOK_COMMAND = '/home/agrif/local/mco-hook/hook.sh'

ROOT_URLCONF = 'overviewer_org.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    project_path('templates'),
)

FIXTURE_DIRS = (
    project_path('fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    
    'django.contrib.markup',
    'typogrify',
    
    'social_auth',
    'social_github',
    
    'uploader',
    'oo_extra',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
