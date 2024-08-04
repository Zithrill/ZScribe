from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ZScribe",
    version="0.10.0",
    author="Jake Gribschaw",
    author_email="jake@zithrill.io",
    description="A tool to generate commit messages and pull request descriptions using various AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zithrill/ZScribe",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic",
        "openai",
        "boto3",
        "requests",
        "click",
    ],
    extras_require={
        "bedrock": ["boto3"],
        "ollama": ["requests"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "zscribe=scribe.zscribe_cli:cli",
        ],
    },
)