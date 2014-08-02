from at_helper.modpack import Modpack

pack = Modpack('YogscastCompletePack')

print('---')
print('Is YogscastCompletePack public?')
print(pack.isPublic())
print('---')
print('What is its full name and description?')
print(pack.name())
print('---')
# print(pack.description())
print('What are its websites?')
print(pack.websites())
print('---')
print('What versions are available?')
print([ v.pack_version for v in pack.versions() ])
print('---')

version = pack.versions()[0]

print('Let\'s compile version ' + version.pack_version + ' with the recommended mods into the folder "full"!')
version.compile('recommended', 'full')
print('---')
print('Now, only include required mods and compile into "slim"!')
version.compile('required', 'slim')
print('---')
print('Get a list of mods!')
version.compile(['Game Mode: Make Powergen Fair', 'TiC Tooltips'], 'thisIsHuge')
print('---')