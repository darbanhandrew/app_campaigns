from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in app_campaigns/__init__.py
from app_campaigns import __version__ as version

setup(
	name="app_campaigns",
	version=version,
	description="Campaigns two show in different places of an app ",
	author="Mohammad Darban Baran",
	author_email="darbanhandrew@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
