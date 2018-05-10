from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='Sticky',
      version='0.1.0',
      description='Sticky Notes',
      url='http://github.com/veeshalsoni/sticky',
      author='Vishal Soni',
      author_email='vishal3soni@gmail.com',
      keywords='StickyNotes Sticky Notes',
      license='GPLv3',
      long_description=readme(),
      classifiers=[
	    'Development Status :: 4 - Beta',
		'Programming Language :: Python',
    	'Intended Audience :: General',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
	  ],
	  pacage_data=,
      install_requires=['PySide'],
      scripts=["initsticky"],
      packages=['sticky'])