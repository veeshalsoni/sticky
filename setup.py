from setuptools import setup
import glob


def readme():
	with open('README.rst') as f:
		return f.read()


setup(
	name='stickynotes',
	version='1.0.0',
	description='Sticky Notes',
	url='http://github.com/veeshalsoni/sticky',
	author='Vishal Soni',
	author_email='vishal3soni@gmail.com',
	keywords='StickyNotes Sticky Notes',
	license='GPLv3',
	long_description=readme(),
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Programming Language :: Python',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
	],
	include_package_data=True,
	install_requires=['PySide2'],
	scripts=['initsticky'],
	packages=['sticky']
)
