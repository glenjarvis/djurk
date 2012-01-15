'''
Created on Jan 10, 2012

@author: Mike_Edwards
'''
from distutils.core import setup

setup(name='django-savvy',
      version='0.01.01-Alpha',
      description='A Django app for accessing Mechanical Turk',
      long_description=open('README.markdown').read(),
      author='Glen Jarvis',
      url='http://djurk.org/',
      license='BSD',
      packages=['djurk', 
                'djurk.migrations',
                'djurk.management'],
      package_dir={'':'src'},
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ]
     )
