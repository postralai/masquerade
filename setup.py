from setuptools import setup
from masquerade import __version__


setup(
    name="masquerade",
    version=__version__,
    description="Python test package",
    url="https://github.com/postralai/masquerade",
    packages=["masquerade"],
    install_requires=open("requirements.txt").read().splitlines(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Filters",
    ],
)