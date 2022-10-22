#!/usr/bin/python3.10

"""
This is the standard runscript for all of calibre's tools.
Do not modify it unless you know what you are doing.
"""

import sys, os

path = os.environ.get('CALIBRE_PYTHON_PATH', '/usr/lib64/calibre')
if path not in sys.path:
    sys.path.insert(0, path)
print(sys.path)

sys.resources_location = os.environ.get('CALIBRE_RESOURCES_PATH', None)
sys.extensions_location = os.environ.get('CALIBRE_EXTENSIONS_PATH', None)
sys.executables_location = os.environ.get('CALIBRE_EXECUTABLES_PATH', None)
sys.system_plugins_location = os.environ.get('CALIBRE_SYSTEM_PLUGINS_PATH', None)
os.environ["CALIBRE_QT_PREFIX"] = os.environ.get("CALIBRE_QT_PREFIX", os.path.expandvars("/usr/lib64/qt6"))

dev_path = os.environ.get('CALIBRE_DEVELOP_FROM')
if  os.environ.get('CALIBRE_WORKER','0') != '1' and\
    dev_path is not None and os.path.isdir(dev_path) and\
    os.path.isdir(dev_path + '/plugins'):
    from calibre.customize.ui import add_plugin
    from calibre import CurrentDir
    from tempfile import NamedTemporaryFile
    from calibre.utils import zipfile
    for entry in os.listdir(dev_path + '/plugins'):
        plugin = dev_path + '/plugins/' + entry
        if entry[0] != '.' and os.path.isdir(plugin):
            print(f'Compressing plugin: {plugin}')
            with NamedTemporaryFile(suffix='.zip') as f:
                with zipfile.ZipFile(f, mode='w', compression=zipfile.ZIP_STORED) as zf:
                    zf.add_dir(plugin, simple_filter=lambda x:(x.startswith('.') or x.endswith('.zip')))
                add_plugin(f.name)
args = sys.argv[1:]
if len(args) < 1:
    args.insert(0, 'calibre')
if args[0] == 'calibre':
    from calibre.gui_launch import calibre as main
    if os.environ.get('CALIBRE_LIBRARY_DIRECTORY') is not None and not '--with-library' in args:
        args += ['--with-library',os.environ.get('CALIBRE_LIBRARY_DIRECTORY')]
    print(sys.argv)
    print(args)
    sys.exit(main(args))
elif args[0] == 'calibre-debug':
    from calibre.debug import main
    if not '--' in args:
        args = args[0] + ['--'] + args[1:]
    print(sys.argv)
    print(args)
    sys.exit(main(args))
elif args[0] == 'calibre-parallel':
    from calibre.utils.ipc.worker import main
    if '--pipe-worker' in args:
        sys.argv = ['calibre-parallel']
        code = ''
        for i in range(1, args.index('--pipe-worker')):
            sys.argv += [args[i]]
        sys.argv += ['--pipe-worker']
        for i in range(args.index('--pipe-worker') + 1, len(args)):
            code += args[i] + ' '
        sys.argv += [code]
    print(sys.argv)
    sys.exit(main())
