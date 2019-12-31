from setuptools import setup

setup(
    name="shotty",
    version="0.1",
    author="John Hillegass",
    author_email="",
    description="A tool to help snapshot AWS EC2 instance volumes",
    license="GPLv3+",
    packages=['shotty'],
    url=[''],
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points = '''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)