from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zscribe",
    version="0.1.2",
    author="Jake Gribschaw",
    author_email="jake@zithrill.io",
    description="A tool to generate commit messages and pull request descriptions using various AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zithrill/ZScribe",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic",
        "openai",
        "boto3",
        "requests",
        "click",
    ],
    tests_require=[
        "pytest",
        "pytest-mock",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pylint",
            "mypy",
            "bandit",
            "types-requests"
        ],
    },
    entry_points={
        "console_scripts": [
            "zscribe=scribe.zscribe_cli:cli",
        ],
    },
)
