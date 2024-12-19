from setuptools import setup, find_packages

NAME="Oasys"

# PACKAGES=["orangeoasys"]

PACKAGES=["orangeoasys",
          "orangeoasys.util",
          "orangeoasys.widgets",
          "orangeoasys.widgets.tools",
          "orangeoasys.widgets.loop_management"]

print(">>>>> PACKAGES: ", PACKAGES)

# PACKAGES=[
#       "orangeoasys",
#       # "orangeoasys.canvas",
#       # "orangeoasys.canvas.styles",
#       # "orangeoasys.menus",
#       "orangeoasys.widgets",
#       "orangeoasys.widgets.tools",
#       "orangeoasys.widgets.scanning",
#       "orangeoasys.widgets.loop_management",
#       ]


PACKAGE_DATA={"orangeoasys": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.util": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.tools": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.loop_management": ["icons/*.svg", "icons/*.png"],
              "orangeoasys.widgets.scanning": ["icons/*.png", "icons/*.svg"],
              }

# PACKAGE_DATA = {
#       # "oasys.application": ["data/*.txt"],
#       # "oasys.canvas": ["icons/*.png", "icons/*.svg"],
#       # "oasys.canvas.styles": ["*.qss", "orange/*.svg"],
#       "orangeoasys": ["icons/*.svg", "icons/*.png"],
#       "orangeoasys.widgets": ["icons/*.svg", "icons/*.png"],
#       "orangeoasys.widgets.tools": ["icons/*.png", "icons/*.svg", "misc/*.png"],
#       "orangeoasys.widgets.loop_management": ["icons/*.png", "icons/*.svg"],
#       "orangeoasys.widgets.scanning": ["icons/*.png", "icons/*.svg"],
# }


CLASSIFIERS=["Example :: Invalid"]
# CLASSIFIERS = (
#       'Development Status :: 5 - Production/Stable',
#       'Environment :: X11 Applications :: Qt',
#       'Environment :: Console',
#       'Environment :: Plugins',
#       'Programming Language :: Python :: 3',
#       'License :: OSI Approved :: '
#       'GNU General Public License v3 or later (GPLv3+)',
#       'Operating System :: POSIX',
#       'Operating System :: Microsoft :: Windows',
#       'Topic :: Scientific/Engineering :: Visualization',
#       'Topic :: Software Development :: Libraries :: Python Modules',
#       'Intended Audience :: Education',
#       'Intended Audience :: Science/Research',
#       'Intended Audience :: Developers',
#       )

# ENTRY_POINTS={"orange.widgets": "Oasys = orangeoasys",}
ENTRY_POINTS={"orange.addons" : ("Oasys = orangeoasys"),
              "orange.widgets": ("Oasys Tools = orangeoasys.widgets.tools",
                                 "Oasys Basic Loops = orangeoasys.widgets.loop_management",
                                 "Oasys Scanning Loops = orangeoasys.widgets.scanning",
                                 ),
              }

# ENTRY_POINTS = {
#       'orange.widgets' : (
#         "Oasys Tools = orangeoasys.widgets.tools",
#         "Oasys Basic Loops = orangeoasys.widgets.loop_management",
#         "Oasys Scanning Loops = orangeoasys.widgets.scanning",
#       )
# }

if __name__ == "__main__":
      setup(name=NAME,
            packages=PACKAGES,
            package_data=PACKAGE_DATA,
            classifiers=CLASSIFIERS,
            # Declare orangedemo package to contain widgets for the "Demo" category
            entry_points=ENTRY_POINTS,
            )

