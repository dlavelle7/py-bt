from setuptools import setup, find_packages

setup(
    name="bt",
    version="1.0.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # TODO: decide on import name
    package_dir={'': '.'},
    include_package_data=True,
)
