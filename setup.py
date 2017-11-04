from setuptools import setup, find_packages
setup(
    name="High Fidelity",
    version="0.1.1",
    author='Barry Loper',
    license='MIT',
    packages=find_packages(),
    python_requires='==3.6.*',
    install_requires=['hug==2.3.2'],
    package_data={'': 'data/albums.csv'},
    entry_points={
        'console_scripts': [
            'hifi-api = hifi.server:main'
         ]
    }
)
