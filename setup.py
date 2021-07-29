from setuptools import setup, find_packages

setup(
    name='django-sage-session',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    version='0.1.0',
    url='https://github.com/sageteam-org/django-sage-cache',
    download_url='https://github.com/sageteam-org/django-sage-cache/archive/refs/tags/0.1.0.tar.gz',
    keywords=['django', 'python', 'session', 'privacy', 'ip'],
    install_requires=[
        'Django'
    ]
)
