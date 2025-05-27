from setuptools import setup

setup(
    name="buildupenglish-bot",
    version="1.0",
    py_modules=["main"],
    install_requires=[
        "python-telegram-bot==20.7"
    ],
    python_requires=">=3.9",
)
