from setuptools import setup

setup(
    name='taskboard-api',
    packages=['taskboard'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pynamodb',
        'python-jose',
    ],
)

