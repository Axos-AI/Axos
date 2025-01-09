import os
from dataclasses import dataclass

import jwt

from .custom_exceptions import BadCredentialsException
from .custom_exceptions import UnableCredentialsException


@dataclass
class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    jwt_access_token: str
    auth0_issuer_url: str = os.getenv("ISSUER")
    auth0_audience: str = os.getenv("AUTH0_API_AUDIENCE")
    algorithm: str = os.getenv("ALGORITHMS")
    jwks_uri = f"{os.getenv('ISSUER')}.well-known/jwks.json"

    def validate(self):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.jwt_access_token).key
            payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
            )
        except jwt.exceptions.PyJWKClientError:
            print(self.auth0_issuer_url)
            print(self.jwt_access_token)
            print(self.algorithm)
            print(self.jwks_uri)
            print("Unable to get signing key from JWT")
            raise UnableCredentialsException
        except jwt.exceptions.InvalidTokenError:
            print("Invalid token")
            raise BadCredentialsException
        return payload
