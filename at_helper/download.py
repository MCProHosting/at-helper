from bs4 import BeautifulSoup
import requests
import hashlib
import shutil
import os
import re
import sys
import unshortenit

if sys.version_info[0] == 3:
    from urllib.parse import quote
else:
    from urllib import quote

class Download():

    item = None
    repo = None

    def __init__(self, repo, item):
        self.repo = repo
        self.item = item

    def _runDownload(self, url, destination, attempt = 0):
        """
        Attempts to download the file into the given destination, checking
        integrity at the same time. It's magic!

        Args:
            url: string for the url to download.
            destination: string of the target path
            attempt: integer signifying the number of the attempted download
        """
        if attempt > 3:
            print('Could not download ' + url)
            return

        # CreeperRepo sometimes replaces one space with two spaces. *shrugs*
        if attempt % 2 != 0:
            url = url.replace(' ', '  ')

        response = requests.get(url, stream=True, allow_redirects=True)
        md5sum = hashlib.md5()
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    md5sum.update(chunk)
                    f.write(chunk)
                    f.flush()

        if md5sum.hexdigest() != self.item.get('md5'):
            print('Corrupt download, retrying...')
            self._runDownload(url, destination, attempt + 1)

    def _downloadServer(self, destination):
        """
        Downloads from CreeperRepo.

        Args:
            destination: string of the destination file.
        """

        self._runDownload(self.repo + '/' + self.item.get('url'), destination)

    def _downloadDirect(self, destination):
        """
        Downloads a direct link.

        Args:
            destination: string of the destination file.
        """

        self._runDownload(self.item.get('url'), destination)

    def _downloadBrowser(self, destination):
        """
        Function which handles browser requires. Resolves adf.ly links as well
        as other shorteners (it does hit them and generate revenue - no bypass),
        and handles Dropbox links as well.

        Args:
            destination: string of the destination file.
        """

        response = requests.get(self.item.get('url'))
        
        if response.status_code != 200:
            print('Failed to download %s with response code %i' % (self.item.get('url'), response.status_code))

        content = BeautifulSoup(response.content)
        pattern = quote(self.item.get('file'))
        link = content.find(href=re.compile(pattern))

        if not link:
            url, status = unshortenit.unshorten(self.item.get('url'))
        else:
            url = link.get('href')

        if not url:
            print('Failed to download %s, could not find a link!' % self.item.get('url'))
            return

        if 'dropbox.com' in url:
            url += '?dl=1'

        self._runDownload(url, destination)

    def downloadTo(self, destination):
        """
        Downloads the current pack to our destination!

        Args:
            destination: string of the destination file.
        """

        try:
            os.makedirs(os.path.dirname(destination))
        except Exception as e:
            pass

        getattr(self, '_download' + self.item.get('download').capitalize())(destination)