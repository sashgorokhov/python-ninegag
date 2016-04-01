from distutils.core import setup

setup(
    requires=['beautifulsoup4', 'requests'],
    name='python-ninegag',
    version='0.1',
    py_modules=['pyninegag'],
    url='https://github.com/sashgorokhov/python-ninegag',
    license='MIT',
    author='sashgorokhov',
    author_email='sashgorokhov@gmail.com',
    description='Python library to get stuff from 9gag.com'
)
