#!/usr/bin/env python
import os, subprocess, shutil
from core import custom
''' Install PyQt from source '''

try:
    from setuptools import setup
except ImportError:
    os.system('apt-get install python-setuptools')
    from setuptools import setup
try:
    import PyQt4
except ImportError:
    os.system('apt-get install python-qt4')

if not os.path.isdir(custom.conf_dir):
    os.mkdir(custom.conf_dir)

if not os.path.isdir(custom.wallets_dir):
    os.mkdir(custom.wallets_dir)


print 'Copying client configuration file'
shutil.copyfile("cryptocurrency/client.conf", custom.conf_file)

uid = int(os.environ.get('SUDO_UID'))
gid = int(os.environ.get('SUDO_GID'))

os.chown(custom.conf_dir, uid, gid)
os.chown(custom.wallets_dir, uid, gid)
os.chown(custom.conf_file, uid, gid)

setup(name='Coinami',
      version='0.1',
      description='Sequence mapping miner',
      url='http://github.com/myozka/coinami',
      author='Coinami Developers',
      author_email='coinamicoin@gmail.com',
      packages=['cryptocurrency', 'ui'],
      install_requires=[
          'numpy',
          'psutil',
          'requests',
          'qdarkstyle'
      ],
      zip_safe=False)