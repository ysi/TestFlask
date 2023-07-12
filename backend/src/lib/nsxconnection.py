#!/opt/homebrew/bin/python3.9
# coding=utf-8

import requests, urllib3
from src.lib import system
from src.constants import constants

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NSX_Session:
    def __init__(self, nsx, login, password, method):
        self.url_session = constants.constants['URL']['SESSION']
        self.url_destroy = constants.constants['URL']['DESTROY_SESSION']
        self.nsx = nsx
        self.login = login
        self.password = password
        self.protocol = constants.constants['DEFAULT']['PROTOCOL']
        self.method = method
        
        if not hasattr(type(self), '_session'):
            self._create_session(self.nsx, self.login, self.password, self.url_session, self.method, self.protocol)

    #####################################################
    # Create a NSX session (cookie or basic auth)
    @classmethod
    def _create_session(cls, nsx, login, password, url_session, method, protocol):

        cls._session = requests.Session()
        cls._session.verify = False

        if method == 'session':
            data = { 'j_username': login,
                'j_password': password
            }
            cls._session.headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Access-Control-Allow-Origin': '*',
                'Accept': '*/*',
                }
            
            result = cls._session.post(protocol + nsx + url_session, data=data)
            if result.status_code == 200:
                print("==> Session authentication: " + system.style.GREEN + "Successful" + system.style.NORMAL)
                cls._session.headers.update({
                    'Content-Type': 'application/json',
                    'X-XSRF-TOKEN': result.headers['x-xsrf-token'],
                    'NSX' : nsx
                    })
        
        if method == 'auth':
            cls._session.auth = (login, password)
            cls._session.headers = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Accept': '*/*',
                }

    #####################################################
    # Close a NSX cookie session
    def destroy_session(self):
        if self.method == 'session':
            result = self._session.post(self.protocol + self.nsx + self.url_destroy)
            if result.status_code == 200:
                print("==> Session destroy: " + system.style.GREEN + "Successful" + system.style.NORMAL)


    #####################################################
    # Get API. Handle the disconnection of a session
    # to do : handle cursor
    def get(self, url):
        retries = 2
        while retries:
            try:
                return self._session.get(self.protocol + self.nsx + url)
            except requests.ConnectionException as e:
                last_connection_exception = e
                retries -= 1
        raise last_connection_exception


