import datetime
import tempfile
import compiler

class Version:

    published = None
    pack_version = None
    pack_name = None
    minecraft_version = None

    path = None

    repo = 'http://www.creeperrepo.net/ATL'

    def __init__(self, name, data):
        self.published = datetime.datetime.fromtimestamp(data['published'])
        self.pack_version = data['version']
        self.pack_name = name
        self.minecraft_version = data['minecraft']

    def compile(self, mods = None, path = None):
        if not path:
            path = tempfile.mkdtemp()

        c = compiler.Compiler(self)

        return c.compile(path, mods)