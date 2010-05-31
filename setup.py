from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='collective.atcassandrastorage',
      version=version,
      description="A AT field storage which stores values to a cassandra database",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone archetype cassandra',
      author='Stefan Eletzhofer',
      author_email='stefan.eletzhofer@inquant.de',
      url='http://github.com/seletz/collective.atcassandrastorage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
