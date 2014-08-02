# at-helper

Open source implementation of the ATLauncher server compilation process. Tell it a pack to make, and it'll create one for you.

> Disclaimer: ATLauncher does not host these pack publicly for a reason: many authors do not allow 3rd party distribution of their mods. Likewise, packs compiled with the at-helper should not be redistributed. This is for private use only.

### CLI Usage:

```
> echo "First you want to install dependencies (one-time thing)"
First you want to install dependencies (one-time thing)

> python setup.py install

> echo "Now, list versions available for YogsCast pack"
Now, list versions available for YogsCast pack

> python at-helper.py YogscastCompletePack
2.9.2.3-RR-YOGS

> echo "Let's build that into folder 'foo'!"
Let's build that into folder 'foo'!

> python at-helper.py YogscastCompletePack --version 2.9.2.3-RR-YOGS --folder foo
```

### Module Usage:

```python
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

version = pack.versions()[0].pack_version

print('Let\'s compile version ' + version + ' with the recommended mods into the folder "full"!')
version.compile('recommended', 'full')
print('---')
print('Now, only include required mods and compile into "slim"!')
version.compile('required', 'slim')
print('---')
print('Get a list of mods!')
version.compile(['Game Mode: Make Powergen Fair', 'TiC Tooltips'], 'thisIsHuge')
print('---')
```

The source is documented, if you're looking for more advanced usages.