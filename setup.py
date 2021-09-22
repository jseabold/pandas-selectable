from setuptools import setup


with open("README.md") as readme:
    description = readme.read()


setup(
    name='pandas_selectable',
    version='1.1.0',
    description='Add a select accessor to pandas',
    packages=['pandas_selectable'],
    long_description=description,
    long_description_content_type="text/markdown",
    author="Skipper Seabold",
    url="https://github.com/jseabold/pandas-selectable",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
