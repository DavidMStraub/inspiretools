from setuptools import setup

setup(name='inspiretools',
      url='https://github.com/DavidMStraub/inspire-tools',
      author='David M. Straub',
      packages=['inspiretools'],
      install_requires=[
        "beautifulsoup4"
      ],
      scripts=['bin/auxtobib','bin/auxtoxml'],
      )
