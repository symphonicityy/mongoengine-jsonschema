import os
import setuptools
from pathlib import Path


NAME = 'mongoengine-jsonschema'

with open('VERSION', 'r') as f:
    VERSION = f.readline().strip('\n')

this_directory = Path(__file__).parent
DESCRIPTION = (this_directory / "README.md").read_text(encoding='utf8')

meta = {
    'version': VERSION,
    'doc': 'MongoEngine JSON Schema Generator',
    'author': 'Yusuf Eroglu',
    'contact': 'myusuferoglu@gmail.com',
    'homepage': "https://github.com/symphonicityy/mongoengine-jsonschema"
}

REQUIREMENTS_FILE = os.getenv('REQUIREMENTS_FILE', 'requirements.txt')


def _strip_comments(line):
    return line.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def reqs(*f):
    """Parse requirement file."""
    return [
        _pip_requirement(r) for r in (_strip_comments(line) for line in open(*f).readlines()) if r]


def install_requires():
    """Get list of requirements required for installation."""
    return reqs(REQUIREMENTS_FILE)


setuptools.setup(
    name=NAME,
    version=meta['version'],
    description=meta['doc'],
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    license='MIT',
    platforms=['any'],
    install_requires=install_requires(),
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Documentation": "https://github.com/symphonicityy/mongoengine-jsonschema/blob/main/README.md",
        "Code": "https://github.com/symphonicityy/mongoengine-jsonschema",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: File Formats :: JSON",
        "Topic :: File Formats :: JSON :: JSON Schema",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Database"
    ]
)
