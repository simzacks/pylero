from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES

import sys

PACKAGE_NAME = "pylarion"
CLI_NAME = "pylarion-cmd"

# change the data dir to be the etc dir under the package dir
for scheme in list(INSTALL_SCHEMES.values()):
    scheme['data'] = '%s/%s/etc' % (scheme['purelib'], PACKAGE_NAME)

install_requires_ = [
    'click',
    'requests>=2.6.0',
    'gnureadline'
]

if sys.version_info >= (3, 0):
    install_requires_.insert(0, 'suds-py3')
else:
    install_requires_.insert(0, 'suds')

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version='0.0.1',
        description="Python SDK for Polarion",
        url="NONE",  # FIXME: once it is public
        author="%s Developers" % PACKAGE_NAME,
        author_email="szacks@redhat.com",
        package_dir={
            PACKAGE_NAME: 'src/%s' % PACKAGE_NAME,
        },
        packages=[
            PACKAGE_NAME,
            PACKAGE_NAME+".cli",
        ],
        scripts=[
            'scripts/%s' % PACKAGE_NAME,
            'scripts/%s' % CLI_NAME,
        ],
        data_files=[
            ('', ['etc/%s/%s.cfg' % (PACKAGE_NAME, PACKAGE_NAME)])
        ],
        install_requires=install_requires_
    )
