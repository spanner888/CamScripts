from setuptools import setup
import os

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "freecad", "cam_scripts", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.cam_scripts',
      version=str(__version__),
      packages=['freecad',
                'freecad.cam_scripts'],
      maintainer="spanner888",
      maintainer_email="spanner888@usabledevices.com",
      url="https://github.com/spanner888/CamScripts",
      description="Powerful automation of CAM tasks",
      install_requires=['numpy',],
      include_package_data=True)
