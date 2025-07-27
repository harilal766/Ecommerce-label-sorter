from setuptools import setup, find_packages
from pathlib import Path

from tests.filepaths import required_dependencies

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="label_sorter",
    version="0.1",
    packages = find_packages(),
    install_requires = required_dependencies,
    author = "Harry19967",
    author_email="harilalsunil2@gmail.com",
    description = "Library to sort Amazon and Shopify shipping labels",
    url= "https://github.com/harilal766/Ecommerce-label-sorter",
    license = "MIT",
    classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent"
    ],
    python_requires = ">=3.9",
    long_description=long_description,
    long_description_content_type='text/markdown'
)