""" API Wrapper for Browserstack Screenshots """

import os

import requests


try:
    import simplejson as json
except ImportError:
    import json


class Screenshots(object):
    """ Browserstack Screenshots API Wrapper """

    DEFAULT_CONFIG = {
        "browsers": [
            {
                "os": "Windows",
                "os_version": "7",
                "browser_version": "8.0",
                "browser": "ie"
            }
        ],
        "url": "http://google.com"
    }

    def __init__(self, **kwargs):
        """
        Create an API instance.
        """
        self.session = requests.Session()
        self.api_url = "http://www.browserstack.com/screenshots"
        if kwargs.get('api_url'):
            self.api_url = kwargs.get('api_url')

        self.config = self.DEFAULT_CONFIG
        if kwargs.get('config'):
            self.config = kwargs.get('config')

        if kwargs.get('auth'):
            if not len(kwargs.get('auth')) == 2:
                raise ImproperlyConfiguredException("Auth is a tuple of \
                    ('username', 'token')")
            self.auth = kwargs.get('auth')
        else:
            raise ImproperlyConfiguredException("Please define an \
                    auth=('username', 'token') tuple in object constructor")

    def _process_response(self, req):
        if req.status_code == 401:
            raise AuthenticationError("Authentication Failure")
        elif req.status_code == 403:
            raise ScreenshotNotAllowedError("Screenshot not allowed")
        elif req.status_code == 422:
            raise InvalidRequestError(**json.loads(req.content))
        elif req.status_code == 200:
            return req
        else:
            raise UnexpectedError(req.status_code)

    def authenticate(self):
        """
        Authenticate with the api
        """
        resp = self.session.get(self.api_url, auth=self.auth)
        resp = self._process_response(resp)
        return resp

    def get_os_and_browsers(self):
        """
        Get all supported OS/browser combinations JSON response
        """
        resp = self.session.get(os.path.join(self.api_url, 'browsers.json'))
        resp = self._process_response(resp)
        return resp.json()

    def generate_screenshots(self):
        """
        Take a config file as input and generate screenshots
        """
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        resp = requests.post(self.api_url, data=json.dumps(self.config), \
                             headers=headers, auth=self.auth)
        resp = self._process_response(resp)
        return resp.json()

    def screenshots_done(self, jobid):
        """
        Return true if the screenshots job is done
        """
        resp = self.session.get(os.path.join(self.api_url, '{0}.json'.format(jobid)))
        resp = self._process_response(resp)
        return True if resp.json()['state'] == 'done' else False

    def get_screenshots(self, jobid):
        """
        Get the jobid JSON response if the screenshots job is done
        """
        resp = self.session.get(os.path.join(self.api_url, '{0}.json'.format(jobid)))
        resp = self._process_response(resp)
        return resp.json() if resp.json()['state'] == 'done' else False


class AuthenticationError(Exception):
    pass


class ScreenshotNotAllowedError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class UnexpectedError(Exception):
    pass


class ImproperlyConfiguredException(Exception):
    pass
