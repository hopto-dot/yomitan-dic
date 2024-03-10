from setuptools import setup, find_packages

setup(
    name='YomitanDic',
    version='0.1.0',
    description='A library for easily creating dictionary files importable into Yomichan for Japanese popup dictionaries',
    author='JawGBoi',
    packages=find_packages(),
    install_requires=[
        "json",
        "os",
        "zipfile",
        "html"
    ],
    python_requires='>=3.6',
)