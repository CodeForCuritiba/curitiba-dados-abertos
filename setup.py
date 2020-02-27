from setuptools import setup, find_namespace_packages


setup(
    name='curitiba-dados-abertos',
    version='1.1.0',
    description='API Used to ease the access to the datasets of Curitiba Dados Abertos portal',
    author='Jonhnatha Trigueiro',
    author_email='joepreludian@gmail.com',
    url='https://github.com/CodeForCuritiba/curitiba-dados-abertos',
    packages=find_namespace_packages(),
    license='MIT License',
    install_requires=[
        'requests (>2.20)'
    ],
    long_description=open('README.md').read()
)
