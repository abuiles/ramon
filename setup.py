from setuptools import setup, find_packages

setup(
    name="ramon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "pydantic",
        "asyncio",
        "pydantic-ai",
        "logfire",
        "devtools",
        "pytest",
        "black",
        "flake8",
        "nanoid",
        "click_default_group"
    ],
    tests_require=[
        "pytest",
        "dirty-equals",
        "anyio",
        "anyio[trio]",
        "trio"

    ],
    entry_points={
        "console_scripts": [
            "ramon=ramon.__main__:cli",
        ],
    },
)
