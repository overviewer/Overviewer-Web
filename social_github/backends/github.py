from django.conf import settings
from social_auth.backends import BaseOAuth2, OAuthBackend

# Backends
class GitHubBackend(OAuthBackend):
    """GitHub OAuth2 authentication backend"""
    name = 'github'

    def get_user_id(self, details, response):
        "Use github username as unique id"""
        print "get_user_id", details
        return details['email']

    def get_user_details(self, response):
        """Return user details from github account"""
        print "get_user_details", response
        email = response['email']
        return {USERNAME: email.split('@', 1)[0],
                'email': email,
                'fullname': '',
                'first_name': '',
                'last_name': ''}

# Auths
class GitHubAuth(BaseOAuth2):
    """GitHub OAuth2 support"""
    AUTH_BACKEND = GitHubBackend
    AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    SETTINGS_KEY_NAME = 'GITHUB_OAUTH2_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'GITHUB_OAUTH2_CLIENT_SECRET'

    def get_scope(self):
        return getattr(settings, 'GITHUB_OAUTH2_EXTRA_SCOPE', [])

    def user_data(self, access_token):
        """Return user data from GitHub API"""
        return {}

BACKENDS = {
    'github' : GitHubAuth,
}
