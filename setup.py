import os

from setuptools import Command, find_packages, setup


def clean_requirements_list(input_list):
    requirements = [r.split("#")[0].strip() for r in input_list]
    return [
        r
        for v in requirements
        if len(r) > 0 and not r.startswith("-") and not r.startswith("git+ssh://") and not r.endswith(".whl")
    ]


class Cleaner(Command):
    def run(self):
        os.system("rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info")


with open("README.md") as f:
    readme = f.read()

with open("requirements/requirements.txt") as f:
    requirements = f.readlines()

requirements = clean_requirements_list(requirements)

setup(
    name="pipeline",
    version="0.0.1",
    description="ZMQ broker pipeline",
    long_description=readme,
    author="Robert Edwards",
    author_email="",
    url="",
    packages=find_packages(include=[], exclude=[]),
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=False,
    keywords="Pump or Dump",
    classifiers=[
        "Intended Audience :: Developers/Researchers",
        "Language :: English",
        "Programming Language :: Python :: 3",
    ],
    cmdclass={"clean": Cleaner},
)