from distutils.core import setup

setup(name='rtml',
      version='0.1.0',
      author="Na'ama Hallakoun",
      author_email='naama@wise.tau.ac.il',
      description='Write RTML plans for ACP Scheduler',
      long_description=open('README.md').read(),
      url='https://github.com/naamach/rtml',
      license='LICENSE.txt',
      py_modules=['rtml'],
      install_requires=['lxml', 'configparser'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Text Processing :: Markup :: XML'
      ]
      )
