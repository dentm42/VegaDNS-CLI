import requests
from requests import auth
import time


class AccessTokenStoreAbstract(object):
    def __init__(self, key, secret, host):
        self.key = key
        self.secret = secret
        self.host = host
        self.now = int(time.time())

    def get(self):
        raise NotImplemented()

    def save(self, access_token, expires_in):
        raise NotImplemented()

    def get_access_token(self):
        token = self.get()
        if token is None:
            newdata = self.get_access_token_from_api()
            self.save(newdata['access_token'], newdata['expires_in'])
            return newdata['access_token']
        else:
            return token

    def get_access_token_from_api(self):
        r = requests.post(
            self.host + "/token",
            auth=auth.HTTPBasicAuth(self.key, self.secret),
            data={"grant_type": "client_credentials"}
        )
        if r.status_code != 200:
            # FIXME error handling
            raise Exception("Error fetching token: " + str(r.status_code))

        return r.json()