from django.conf import settings
from django.utils import simplejson
from django.contrib.auth import authenticate
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME

from urllib import urlencode
from urllib2 import Request, urlopen
from urlparse import parse_qs

GITHUB_API_USERINFO = 'https://api.github.com/user'

# Backends
class GitHubBackend(OAuthBackend):
    """GitHub OAuth2 authentication backend"""
    name = 'github'

    def get_user_id(self, details, response):
        "Use github username as unique id"""
        print "get_user_id", details
        return details[USERNAME]

    def get_user_details(self, response):
        """Return user details from github account"""
        print "get_user_details", response
        email = response.get('email', None)
        if email is None:
            email = ''
        name = response.get('name', None)
        if name is None:
            name = ''
        return {USERNAME: response['login'],
                'email': email,
                'fullname': name,
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
        
        headers = {'Authorization': 'token %s' % access_token}
        request = Request(GITHUB_API_USERINFO, headers=headers)
        
        try:
            response = simplejson.loads(urlopen(request).read())
        except (ValueError, KeyError):
            raise ValueError('Unknown GitHub API response type')
        
        return response

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        # we override this because GitHub responds with urlencoded data,
        # not json like BaseOAuth2 expects
        client_id, client_secret = self.get_key_and_secret()
        params = {'grant_type': 'authorization_code',  # request auth code
                  'code': self.data.get('code', ''),  # server response code
                  'client_id': client_id,
                  'client_secret': client_secret,
                  'redirect_uri': self.redirect_uri}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=headers)

        try:
            response = parse_qs(urlopen(request).read())
        except (ValueError, KeyError):
            raise ValueError('Unknown OAuth2 response type')

        if response.get('error'):
            error = response.get('error_description') or response.get('error')
            raise ValueError('OAuth2 authentication failed: %s' % error)
        else:
            response_only_one = {}
            for k in response:
                response_only_one[k] = response[k][0]
            response = response_only_one
            response.update(self.user_data(response['access_token']) or {})
            kwargs.update({'response': response, self.AUTH_BACKEND.name: True})
            return authenticate(*args, **kwargs)

BACKENDS = {
    'github' : GitHubAuth,
}
