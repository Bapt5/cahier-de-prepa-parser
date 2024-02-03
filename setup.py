import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cahier-de-prepa-parser",
    version="1.0.2",
    description="Python parser pour Cahier de Prépa",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords = ["cahier de prépa", "parser"],
    url="https://www.github.com/Bapt5/cahier-de-prepa-parser",
    download_url="https://github.com/Bapt5/cahier-de-prepa-parser/archive/refs/tags/v1.0.2.tar.gz",
    author="Bapt5",
    author_email='drouillet.baptiste@gmail.com',
    license="MPL2.0",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.21.0",
        "beautifulsoup4>=4.12.0",
    ]
)