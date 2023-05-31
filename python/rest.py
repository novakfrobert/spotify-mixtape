import requests
from urllib.parse import urlencode
import json


class RestRequest:

    def __init__(self, base_url, default_headers = None):
        self.base_url = base_url
        self.default_headers = default_headers

    def get_full_url(self, endpoint, params = None):
        """
        """

        url = self.base_url + endpoint 

        if params != None:
            query_string = urlencode(params)
            url += "/?" + query_string
        
        return url


    def get(self, url):
        return requests.get(url)


    def get(self, endpoint=None, params=None, url_override=None):

        if url_override is None:
            url = self.get_full_url(endpoint, params)
        else:
            url = url_override

        print()
        print("Sending HTTP GET Request: ")
        print(self.default_headers)
        print(url)
        print()

        return requests.get(url=url, headers=self.default_headers)


    def post(self, endpoint, payload, urlparams = None):

        url = self.get_full_url(endpoint, urlparams)

        print()
        print("Sending HTTP POST Request: ")
        print(self.default_headers)
        print(url)
        print(payload)
        print()

        return requests.post(url=url, data=json.dumps(payload), headers=self.default_headers)
