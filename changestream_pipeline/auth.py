import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

import jwt
import requests

from config import JWT_EXPIRY


class AuthenticationError(Exception):
    pass


class Authoriser(ABC):

    def __init__(self):
        self.err = None
        self.token = None
        self.credentials = None

    def get_credentials_from_file(self, path_to_file: Union[str, Path]):
        with open(path_to_file, 'r') as f:
            self.credentials = json.loads(f.read())

    @abstractmethod
    def _create_signed_jwt(self):
        pass

    @abstractmethod
    def _generate_access_token(self):
        pass

    def get_token(self):
        return self.token


class OAUTHoriser(Authoriser):

    def __init__(self):
        super().__init__()
        self.jwt = None
        self.oauth_token = None

    def authenticate(self):
        if self.credentials is None:
            raise AuthenticationError('No authentication credentials available, please load authentication credentials')

        self.jwt = self._create_signed_jwt()
        self.oauth_token = self._generate_access_token()

        return self.oauth_token

    def _create_signed_jwt(self) -> str:

        issued = int(time.time())
        expires = issued + JWT_EXPIRY

        headers = {
            'kid': self.credentials['private_key_id'],
            'alg': "RS256",
            'typ': "JWT",
        }

        payload = {
            "iss": self.credentials['client_email'],
            "sub": self.credentials['client_email'],
            "aud": self.credentials['token_uri'],
            "iat": issued,
            "exp": expires,
            "scope": "https://www.googleapis.com/auth/spanner.data"
        }

        sig = jwt.encode(payload, self.credentials['private_key'], algorithm="RS256", headers=headers)
        return sig

    def _generate_access_token(self) -> str:
        auth_url = self.credentials['token_uri']

        params = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": self.jwt
        }

        r = requests.post(auth_url, data=params)

        if r.ok:
            return r.json()['access_token']

        raise Exception(r.text)

    def get_token(self, credentials=None):
        if self.oauth_token is not None:
            return self.oauth_token
        else:
            raise AuthenticationError("Please authenticate before requesting a token")
