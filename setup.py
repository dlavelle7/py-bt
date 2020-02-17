from setuptools import setup, find_packages

deps = [
    "PyYAML==5.3",
]

setup(
    name="py-bt",
    version="0.0.1",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=deps,
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
