from setuptools import setup, find_packages

setup(
    name="buildup-english-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot[all]==20.7",
    ],
    python_requires=">=3.8",
)
