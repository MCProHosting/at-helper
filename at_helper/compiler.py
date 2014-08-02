from bs4 import BeautifulSoup, Tag
import zipfile
import os.path
import distutils.dir_util
import shutil
import requests

from at_helper.download import Download

class Compiler:

    version = None
    mods = None
    path = None

    repo = 'http://www.creeperrepo.net/ATL'

    def __init__(self, version):
        self.version = version


    def _downloadTo(self, item, destination):
        """
        Attempts to download the URL into the modpack. Does check integrity.

        Args:
            item: Etree element of the item to download.
            destination: String of the file path relative to the target
                folder base, into which the file should be downloaded.
        """

        dl = Download(self.repo, item)
        dl.downloadTo(os.path.join(self.path, destination))
    
    def _compileLibraries(self, library):
        """
        Places the library in the target folder.

        Args:
            library: The LXML element representing the current library.
        Returns:
            void
        """

        if not library.get('server'):
            return

        self._downloadTo(library, os.path.join('libraries', library.get('server')))


    def _compileMods(self, mod):
        """
        Places the mod appropriately in the target folder.

        Args:
            mod: The LXML element representing the current mod.
        Returns:
            void
        """

        if mod.get('optional') == 'yes':
            if self.mods == 'required':
                return

            if isinstance(self.mods, list) and not mod.get('name') in self.mods:
                return

            if self.mods == 'recommended' and not mod.get('recommended') == 'yes':
                return

        type = mod.get('type')

        if type == 'forge':
            self._downloadTo(mod, mod.get('file'))
        elif type == 'dependency':
            self._downloadTo(mod, os.path.join('mods', self.version.minecraft_version, mod.get('file')))
        elif type == 'mods':
            self._downloadTo(mod, os.path.join('mods', mod.get('file')))
        elif type =='extract':
            tempZip = os.path.join(self.path, os.path.join('.temp', mod.get('file')))
            base, extension = os.path.splitext(tempZip)

            self._downloadTo(mod, os.path.join('.temp', mod.get('file')))

            # with zipfile.ZipFile(tempZip) as z:
            #     z.extractall(base)

            # distutils.dir_util.copy_tree(base, os.path.join(self.path, mod.get('extractto').replace('root', '')))
            # shutil.rmtree(os.path.join(self.path, '.temp'))


    def getRecipe(self):
        """
        Gets the XML "recipe" from CreeperRepo in order to compile the modpack.

        Returns:
            An LXML element representing the recipe.
        """
        response = requests.get('%s/packs/%s/versions/%s/Configs.xml' % (self.repo, self.version.pack_name, self.version.pack_version))
        
        if response.status_code != 200:
            raise RuntimeError(response.status_code , 'Bad response code from CreeperRepo API')

        return BeautifulSoup(response.content, 'xml')


    def compile(self, path, mods = None):
        """
        Compiles the modpack.

        Args:
            path: Path to compile the modpack into.
            mods: This can be a list or string. It may be a list of mod names to
                install, though this is not normally recommended. Or, it can be
                "required" or "recommended", to install the required mods or
                "recommended" mods for the pack. If None, every mod will be
                installed.
        Returns:
            void
        """
        self.path = path
        self.mods = mods

        recipe = self.getRecipe()

        try:
            shutil.rmtree(self.path)
        except Exception:
            pass

        for task in ['libraries', 'mods']:
            task_list = getattr(recipe, task)

            if task_list == None: continue

            for child in task_list.children:
                if not isinstance(child, Tag): continue

                getattr(self, '_compile' + task.capitalize())(child)