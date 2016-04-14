from setuptools import setup
import py2exe

setup (
    name = "RabbitHole",
    version = "1.0.0",
    description="RabbitHole is a RabbitMQ message utility.",
    author="Greg Major",
    author_email="", # Removed to limit spam harvesting.
    url="http://www.leadpipesoftware.com/",
    packages=['RabbitHole'],
    entry_points = {
        'console_scripts': ['RabbitHole = RabbitHole.__main__:main']
                    },
    download_url = "http://www.leadpipesoftware.com/",
    zip_safe = True
)
