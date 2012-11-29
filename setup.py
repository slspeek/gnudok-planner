from setuptools import setup, find_packages

setup(
    name = "planner",
    version = "1.0",
    url = 'http://code.google.com/p/gnudok-planner/',
    license = 'GPL',
    description = "Planner for Juttersdok",
    author = 'Steven Speek',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools',
                        'factory_boy',
                        'docutils',
                        'django-bootstrap-toolkit',
                        'django',
                        'django-nose', 
                        'django_jenkins',
                        'selenium',
                        'MySQL-python'],
)
