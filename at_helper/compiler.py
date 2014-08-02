import lxml.etree
import zipfile
import requests
import os
import os.path
import distutils.dir_util
import shutil
import hashlib

class Compiler:

    version = None
    mods = None
    path = None

    def __init__(self, version):
        self.version = version


    def _downloadTo(self, url, destination, md5sum_verify = None, attempt = 0):

        target = os.path.join(self.path, destination)
        try:
            os.makedirs(os.path.dirname(target))
        except Exception as e:
            pass

        final_url = self.version.repo + '/' + url
        # CreeperRepo sometimes replaces one space with two spaces. *shrugs*
        if attempt % 2 != 0:
            final_url = final_url.replace(' ', '  ')

        print 'Now downloading ' + final_url
        response = requests.get(final_url, stream=True)
        md5sum = hashlib.md5()
        with open(target, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    md5sum.update(chunk)
                    f.write(chunk)
                    f.flush()

        if md5sum.hexdigest() != md5sum_verify:
            print 'Corrupt download, retrying...'
            self._downloadTo(url, destination, md5sum_verify, attempt + 1)
    
    def _compileLibraries(self, recipe, library):
        if library.get('download') != 'server':
            print 'Skipping download of %s because download type is %s' % (library.get('file'), library.get('download'))
            return

        if not library.get('server'):
            return

        self._downloadTo(library.get('url'), os.path.join('libraries', library.get('server')), library.get('md5'))


    def _compileMods(self, recipe, mod):
        if mod.get('download') != 'server':
            print 'Skipping download of %s because download type is %s' % (mod.get('name'), mod.get('download'))
            return

        if mod.get('optional') == 'yes':
            if isinstance(self.mods, list) and not mod.get('name') in self.mods:
                print 'Skipping download of %s because it is not in our list' % mod.get('name')
                return

            if self.mods == 'recommended' and not mod.get('recommended') == 'yes':
                print 'Skipping download of %s because it is not recommended' % mod.get('name')
                return


        type = mod.get('type')

        if type == 'forge':
            self._downloadTo(mod.get('url'), mod.get('file'), mod.get('md5'))
        elif type == 'dependency':
            self._downloadTo(mod.get('url'), os.path.join('mods', self.version.minecraft_version, mod.get('file')), mod.get('md5'))
        elif type == 'mods':
            self._downloadTo(mod.get('url'), os.path.join('mods', mod.get('file')), mod.get('md5'))
        elif type =='extract':
            tempZip = os.path.join(self.path, os.path.join('.temp', mod.get('file')))
            base, extension = os.path.splitext(tempZip)

            self._downloadTo(mod.get('url'), os.path.join('.temp', mod.get('file')), mod.get('md5'))

            with zipfile.ZipFile(tempZip) as z:
                z.extractall(base)

            distutils.dir_util.copy_tree(base, os.path.join(self.path, mod.get('extractto').replace('root', '')))
            shutil.rmtree(os.path.join(self.path, '.temp'))


    def getRecipe(self):
        with open('testTree.xml') as f:
            return lxml.etree.fromstring(f.read())

        response = requests.get('%s/packs/%s/versions/%s/Configs.yml' % (self.version.repo, self.version.pack_name, self.version.pack_version))

        if response.status_code != 200:
            raise Exception('Bad response code ' + response.status_code + ' from ATLauncher API')

        return lxml.etree.fromstring(response.content)


    def compile(self, path, mods = None):
        self.path = path
        self.mods = mods

        recipe = self.getRecipe()

        shutil.rmtree(self.path)
        for task in ['libraries', 'mods']:
            task_list = recipe.find(task)

            if not task_list: continue

            for child in task_list:
                getattr(self, '_compile' + task.capitalize())(recipe, child)