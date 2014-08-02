import requests
from at_helper.version import Version

class Modpack:

    slug = None
    version_data = None

    api = 'https://api.atlauncher.com/v1/'

    def __init__(self, slug):
        """
        Creates a modpack object, using the given slug.

        Args:
            slug: Slug for the modpack, same as the `safeName`
                from the ATLauncher API.
        """

        self.slug = slug

    def _getData(self):
        """
        Gets and parses version data from the ATLauncher API.

        Returns:
            A dict corresponding to the "data" in the API. Notably, the "versions"
            array has been replaced with a list of Version objects.
        Throws:
            RuntimeError: If we're unable to access to the ATLauncher API.
        """

        if not self.version_data:
            response = requests.get(self.api + 'pack/' + self.slug + '/')

            if response.status_code != 200 or response.json()['error']:
                raise RuntimeError(response.status_code, 'Bad response code from ATLauncher API.')

            self.version_data = response.json()['data']
            self.version_data['versions'] = map(lambda v: Version(self.slug, v), self.version_data['versions'])

        return self.version_data

    def versions(self):
        """
        Get modpack versions.

        Returns:
            A list of Version objects appropriate to the modpack.
        """
        return self._getData()['versions']

    def isPublic(self):
        """
        Determines whether the modpack in question is public or not.
        
        Returns:
            True if the pack is public, false if it is not.
        """
        return self._getData()['type'] == 'public'

    def name(self):
        """
        Gets the name of the modpack.

        Returns:
            String of the modpack name.
        """
        return self._getData()['name']

    def description(self):
        """
        Gets the modpack description.

        Returns:
            String of the description.
        """

        return self._getData()['description']

    def websites(self):
        """
        Gets websites for the modpack.

        Returns:
            A dict with keys "support" for the support website, and "modpack"
            for the primary modpack website.
        """
        return {
            'support': self._getData()['supportURL'],
            'modpack': self._getData()['websiteURL']
        }