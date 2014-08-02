import datetime
import tempfile
from at_helper.compiler import Compiler

class Version:

    published = None
    pack_version = None
    pack_name = None
    minecraft_version = None

    path = None

    def __init__(self, name, data):
        """
        Creates a Version object.

        Args:
            name: The string slug of the modpack this is a child of.
            data: Dict of data for the version, from the ATLauncher API. It
                should have the keys "version", "minecraft", and "published".
                These should be the modpack version, Minecraft version it is
                for, and the unix timestamp of its release, respectively.
        """

        self.published = datetime.datetime.fromtimestamp(data['published'])
        self.pack_version = data['version']
        self.pack_name = name
        self.minecraft_version = data['minecraft']

    def compile(self, mods = None, path = None):
        """
        Compiles the version!

        Args:
            mods: This can be a list or string. It may be a list of mod names to
                install, though this is not normally recommended. Or, it can be
                "required" or "recommended", to install the required mods or
                "recommended" mods for the pack. If None, every mod will be
                installed.
            path:
                Path to compile it to. Directory will be created if it doesn't
                already exist. If no path is given, a temporary path will be
                made. You are responsible for removing the temporary folder
                after you are finished with it.
        Returns:
            void
        Throws:
            RuntimeError if there is a breaking issue with compilation.
        """
        if not path:
            path = tempfile.mkdtemp()

        c = Compiler(self)

        return c.compile(path, mods)