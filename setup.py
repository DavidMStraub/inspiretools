from setuptools import setup

setup(name='inspiretools',
      version='0.2.1',
      url='https://github.com/DavidMStraub/inspire-tools',
      author='David M. Straub',
      packages=['inspiretools'],
      install_requires=[
        "beautifulsoup4"
      ],
      entry_points={
        'console_scripts': [
            'auxtobib = inspiretools:aux2bib',
            'auxtoxml = inspiretools:aux2xml',
            'blgtobib = inspiretools:blg2bib',
        ]
      }
      )
