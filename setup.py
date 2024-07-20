from setuptools import setup


entry_points = {"console_scripts": ["python2latex = lathon:python2latex"]}

setup(name='lathon',
      version=str("0.0.1"),
      py_modules=['lathon'],
      entry_points=entry_points,
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/FCGear",
      description="python equations documented with latex",
	include_package_data=True
)
