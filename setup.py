from setuptools import setup
from pygears import __version__

setup(name='lathon',
      version=str(__version__),
      py_modules=['lathon'],
      scripts=['python2latex'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/FCGear",
      description="python equations documented with latex",
	  include_package_data=True
)
