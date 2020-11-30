from setuptools import setup

setup(name='inspiretools',
      version='0.3',
      url='https://github.com/DavidMStraub/inspire-tools',
      author='David M. Straub',
      packages=['inspiretools'],
      install_requires=[
        "requests
      ],
      entry_points={
        'console_scripts': [
            'auxtobib = inspiretools:aux2bib',
            'blgtobib = inspiretools:blg2bib',
        ]
      }
      )
