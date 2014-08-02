from at_helper.modpack import Modpack
import argparse
import sys

parser = argparse.ArgumentParser(description='CLI application to build ATLauncher modpacks.')
parser.add_argument('modpack', help='The slug of the modpack. If versions is not given, it will list the versions available.')
parser.add_argument('--version', help='Version of the modpack to build.')
parser.add_argument('--folder', help='Destination folder to build into.')
parser.add_argument('--compile', default='recommended', help='Which mods to compile. Can be one of: "recommended", "required".')

args = parser.parse_args()

modpack = Modpack(args.modpack)

try:
    versions = modpack.versions()
except RuntimeError as e:
    print('Error from ATLauncher API: %i. Perhaps there is a typo in the modpack name?' % e.args[0])
    sys.exit(1)

if args.version != None:
    if args.folder == None:
        print('You must specify the folder you want to build into!')
        sys.exit(1)

    target_version = None
    for v in versions:
        if v.pack_version == args.version:
            target_version = v

    if target_version == None:
        print('Version not found!')
        sys.exit(1)

    target_version.compile(['AnimationAPI'], args.folder)
else:
    for v in versions:
        print(v.pack_version)