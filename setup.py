from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="git-commit-message-generator",
    version="0.2.0",  # Updated version
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to generate commit messages using the Anthropic API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/git-commit-message-generator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "anthropic",
    ],
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
            "git-commit-message-generator=commit_message_generator.main:main",
        ],
    },
)