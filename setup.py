#!/usr/bin/env python3

from setuptools import setup

setup(
    name="project_amber",
    version="0.0.4",
    description="The backend app of a note-taking app, Project Amber",
    url="https://git.tdem.in/tdemin/amber",
    author="Timur Demin",
    author_email="me@tdem.in",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha", "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
        "Programming Language :: Python :: 3"
    ],
    keywords="tasks backend flask",
    project_urls={"Homepage": "https://git.tdem.in/tdemin/amber"},
    packages=["project_amber"],
    install_requires=["flask", "flask-cors", "flask-sqlalchemy", "bcrypt"],
    python_requires=">=3.6"
)
