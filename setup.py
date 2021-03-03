import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ADS1x15-ADC",
    version="1.1.0",
    description="Python library used for ADS1x15 analog to digital converter (ADC)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chandrawi/ADS1x15-ADC",
    author="Chandra Wijaya Sentosa",
    author_email="chandra.w.sentosa@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=[
        "ADS1x15", 
    ],
    include_package_data=True,
    install_requires=[
        "smbus2",
    ],
)
