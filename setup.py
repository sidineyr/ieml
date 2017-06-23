from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='ieml',
      version='0.1',
      description='Implementation of the artificial natural language IEML',
      long_description=readme(),
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3.5',
            'Topic :: Text Processing :: Linguistic',
            'Topic :: Text Processing :: Indexing'
      ],
      keywords='ieml semantic syntax relations',
      url='https://github.com/IEMLdev/ieml',
      author='Louis van Beurden',
      author_email='louis.vanbeurden@gmail.com',
      license='GPLv3',
      packages=['ieml'],
      install_requires=[],
      test_suite='nose2.collector.collector',
      tests_require=['nose2'],
      include_package_data=True,
      zip_safe=False)