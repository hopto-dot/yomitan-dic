1. Increment the version number in `setup.py`
2. Delete `dist` directory
3. `python setup.py sdist bdist_wheel`
4. `twine upload dist/*`
5. Get working api token from https://pypi.org/manage/account/token/ - type this in the console