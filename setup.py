from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in customization/__init__.py
from customization import __version__ as version

setup(
	name="customization",
	version=version,
	description="Customizations to our ERPNext instance",
	author="intelli-Momentum GmbH",
	author_email="bernhard.hein@intelli-Momentum.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
