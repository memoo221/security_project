from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#") and not line.startswith("-e")]

setup(
    name="networksecurity",
    version="0.0.1",
    author="Access",
    packages=find_packages(),
    install_requires=requirements
)
