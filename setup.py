import os
import setuptools

NAME = 'mongoengine-jsonschema'

with open('VERSION', 'r') as f:
    VERSION = f.readline().strip('\n')

meta = {
    'version': VERSION,
    'doc': 'MongoEngine JSON Schema Generator',
    'description': "This package provides a mixin class that extends a MongoEngine document's functionality by adding a .json_schema() method and allows generating a JSON schema directly from the document. Generated schema then can be used in API documentation or form validation and automatic form generation on a web application frontend, etc.",
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
    long_description=meta['description'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    license='MIT',
    platforms=['any'],
    install_requires=install_requires(),
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.10",
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
