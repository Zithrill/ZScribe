from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ZScribe",
    version="0.8.0",
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
    ],
    extras_require={
        "bedrock": ["boto3"],
        "ollama": ["requests"],
        "llm_studio": [],  # Add any specific requirements for LLM Studio
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
            "zscribe=scribe.main:main",
            "zscribe-prepare-commit-msg=scribe.prepare_commit_msg:main",
            "zscribe-manage-hooks=scribe.setup_git_hook:setup_git_hooks",
            "zscribe-pr-hook=scribe.pr_hook_script:main",
        ],
    },
)