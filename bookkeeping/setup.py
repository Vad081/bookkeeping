from setuptools import setup

setup(
    name='task-bookkeeping',
    version='0.0.0',
    description='Console bookkeeping.',
    license='Apache License 2.0',
    author='Vadim Ayupov',
    author_email='aupovv@gmail.com',
    packages=['task_bookkeeping'],
    entry_points={
        'console_scripts': [
            'bkp = task_bookkeeping:main',
        ],
    },
    install_requires=[
        'appdirs',
        'prettytable',
    ],
    package_data={
        'task_bookkeeping': ['resources/*'],
    }
)
