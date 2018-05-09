from setuptools import setup

setup(name='Sticky',
      version='0.1.0',
      description='Sticky Notes',
      url='http://github.com/veeshalsoni/sticky',
      author='Vishal Soni',
      author_email='vishal3soni@gmail.com',
      license='GPLv3',
      install_requires=['PySide'],
      scripts=["initsticky"],
      packages=['sticky'])