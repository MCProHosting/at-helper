import requests
from version import Version

class Modpack:

    slug = None
    version_data = None
    urls = {
        'atlauncher': 'https://api.atlauncher.com/v1/',
        'creeperrepo': 'http://www.creeperrepo.net/ATL/packs/'
    }

    def __init__(self, slug):
        self.slug = slug

    def _getData(self):
        if not self.version_data:
            response = requests.get(self.urls['atlauncher'] + 'pack/' + self.slug + '/')

            if response.status_code != 200 or response.json()['error']:
                return False

            self.version_data = response.json()['data']
            self.version_data['versions'] = map(lambda v: Version(v), self.version_data['versions'])

        return self.version_data

    def versions(self):
        return self._getData()['versions']

    def isPublic(self):
        return self._getData()['type'] == 'public'

    def name(self):
        return self._getData()['name']

    def description(self):
        return self._getData()['description']

    def websites(self):
        return {
            'support': self._getData()['supportURL'],
            'modpack': self._getData()['websiteURL']
        }