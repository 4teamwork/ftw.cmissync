from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ftw.cmissync',
      version=version,
      description="Allows synchronization between Plone content and CMIS objects.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Thomas Buchberger',
      author_email='t.buchberger@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.cmissync',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'cmislib',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
