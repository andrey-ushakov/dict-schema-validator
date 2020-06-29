import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dict-schema-validator",
    version="0.1.2",
    author="Andrey U",
    description="Validate python dictionaries (mongodb docs etc) using a JSON schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrey-ushakov/dict-schema-validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)