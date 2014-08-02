import datetime

class Version:

    published = None
    pack_version = None
    minecraft_version = None

    def __init__(self, data):
        self.published = datetime.datetime.fromtimestamp(data['published'])
        self.pack_version = data['version']
        self.minecraft_version = data['minecraft']