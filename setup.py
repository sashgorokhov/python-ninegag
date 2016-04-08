from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    requires=['beautifulsoup4', 'requests'],
    name='python-ninegag',
    version='0.4',
    py_modules=['pyninegag'],
    url='https://github.com/sashgorokhov/python-ninegag',
    download_url='https://github.com/sashgorokhov/python-ninegag/archive/master.zip',
    keywords=['ninegag', '9gag'],
    classifiers=[],
    long_description=long_description,
    license='MIT License',
    author='sashgorokhov',
    author_email='sashgorokhov@gmail.com',
    description='Python library to get stuff from 9gag.com'
)
