from os.path import join, dirname

from setuptools import setup, find_packages


def load_doc():
    with open(join(dirname(__file__), 'README.rst')) as file:
        return file.read()


setup(
    name='hawkcatcher',
    version='2.0.0',
    packages=find_packages(),
    description='Python errors Catcher module for Hawk.',
    long_description=load_doc(),
    keywords='catcher hawk codex bug errors tracker',
    url='https://github.com/codex-team/deployserver',
    author='CodeX Team',
    author_email='team@ifmo.su',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Bug Tracking',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Environment :: Web Environment',
    ],
    install_requires=['requests'],
    python_requires='>=3.5'
)
