import cmds
try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

setup(name="rops",
      version='0.1',
      author='Ali Ikram',
      entry_points={
        'console_scripts': 'rops=cmds.ropslaunch:main',
        },
      author_email='aikram24@hotmail.com',
      install_requires=['boto3','argparse'],
      packages=find_packages())
