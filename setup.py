from setuptools import setup
import os

NAME="Oasys"

PACKAGES=["orangeoasys",
          "orangeoasys.util",
          "orangeoasys.widgets",
          "orangeoasys.widgets.tools",
          "orangeoasys.widgets.loop_management"]

PACKAGE_DATA={"orangeoasys": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.util": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.tools": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.loop_management": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.scanning": ["icons/*.png", "icons/*.svg"],
              }


# CLASSIFIERS=["Example :: Invalid"]
CLASSIFIERS = (
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
)

ENTRY_POINTS={"orange.addons" : ("Oasys = orangeoasys"),
              "orange.widgets": ("Oasys Tools = orangeoasys.widgets.tools",
                                 "Oasys Basic Loops = orangeoasys.widgets.loop_management",
                                 "Oasys Scanning Loops = orangeoasys.widgets.scanning",
                                 ),
              }
#
#
#
VERSION = '0.0.1'
DESCRIPTION = 'OrAnge SYnchrotron Suite'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE).read()


AUTHOR = 'Luca Rebuffi, Manuel Sanchez del Rio and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'lrebuffi@anl.gov'
MAINTAINER = 'Luca Rebuffi, Argonne National Lab, USA'
MAINTAINER_EMAIL = 'lrebuffi@anl.gov'
URL = 'https://github.com/srio/orange-oasys'
DOWNLOAD_URL = 'https://github.com/srio/orange-oasys'
LICENSE = 'MIT'
KEYWORDS = (
    'synchrotron',
    'simulation',
)


SETUP_REQUIRES = (
    'setuptools',
)

INSTALL_REQUIRES = (
    # 'setuptools',
    # 'requests',
    # 'numpy<1.23,>=1.21',
    # 'fabio==0.11.0',
    # 'PyQt5==5.15.2',
    'scipy',
    # 'matplotlib<=3.5.3,>=3.3.2',
    # 'oasys-canvas-core>=1.0.7',
    # 'oasys-widget-core>=1.0.3',
    'silx',
    'hdf5plugin',
    'srxraylib',
    'syned',
    'wofry',
)

CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: '
    'GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
)



if __name__ == "__main__":
      setup(name=NAME,
            packages=PACKAGES,
            package_data=PACKAGE_DATA,
            classifiers=CLASSIFIERS,
            # Declare orangedemo package to contain widgets for the "Oasys" category
            entry_points=ENTRY_POINTS,
            #
            version=VERSION,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            keywords=KEYWORDS,
            # extra setuptools args
            zip_safe=False,  # the package can run out of an .egg file
            include_package_data=True,
            install_requires=INSTALL_REQUIRES,
            setup_requires=SETUP_REQUIRES,
            )

