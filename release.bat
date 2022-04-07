cls
RD /S /Q "%cd%\build"
RD /S /Q "%cd%\dist"
python setup.py sdist bdist_wheel
python -m twine upload -r testpypi dist/*