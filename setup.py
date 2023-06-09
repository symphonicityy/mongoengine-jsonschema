import os
import setuptools


NAME = 'mongoengine-jsonschema'

with open('VERSION', 'r') as f:
    VERSION = f.readline().strip('\n')

meta = {
    'version': VERSION,
    'doc': 'MongoEngine JSON Schema Generator',
    'author': 'Yusuf Eroglu',
    'contact': 'yusuf.eroglu@btsgrp.com',
    # 'homepage': 'https://btslabs.ai/',
}

REQUIREMENTS_FILE = os.getenv('REQUIREMENTS_FILE', 'requirements.txt')


def _strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def reqs(*f):
    """Parse requirement file."""
    return [
        _pip_requirement(r) for r in (_strip_comments(l) for l in open(*f).readlines()) if r]


def install_requires():
    """Get list of requirements required for installation."""
    return reqs(REQUIREMENTS_FILE)


setuptools.setup(
    name=NAME,
    version=meta['version'],
    description=meta['doc'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    license='Proprietary',
    platforms=['any'],
    install_requires=install_requires(),
    python_requires=">=3.10",
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Documentation": "https://github.com/symphonicityy/mongoengine-jsonschema/README.md",
        "Code": "https://github.com/symphonicityy/mongoengine-jsonschema",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ]
)