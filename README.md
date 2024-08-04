# ZithScribe

ZithScribe is a command-line tool that automatically generates meaningful commit messages using the Anthropic API. By analyzing the differences between git commits, it provides concise and informative commit messages, saving developers time and improving the quality of version control documentation.

## Features

- Generates commit messages based on git diffs
- Uses Anthropic's AI to create human-readable, context-aware messages
- Supports refinement of generated messages for improved accuracy
- Easy to use command-line interface
- Can be integrated as a Git hook for automatic commit message generation
- Automated setup of Git hook

## Installation

To install ZithScribe, you can use pip:

```bash
pip install zithScribe
```

## Usage

Before using ZithScribe, make sure to set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### As a standalone tool

To generate a commit message, use the following command:

```bash
zithScribe <commit1> <commit2>
```

Replace `<commit1>` and `<commit2>` with the commit hashes you want to compare. For example:

```bash
zithScribe HEAD~1 HEAD
```

This will generate a commit message based on the changes between the current HEAD and the previous commit.

To use the refinement feature, add the `--refine` flag:

```bash
zithScribe HEAD~1 HEAD --refine
```

### Setting up the Git hook

To use ZithScribe automatically when you make a commit, you can set it up as a Git hook. We've provided a script to automate this process:

1. Navigate to your Git repository:
   ```
   cd /path/to/your/repo
   ```

2. Run the setup script:
   ```
   zithScribe-setup-hook
   ```

This script will create the necessary Git hook in your repository. Now, whenever you run `git commit`, ZithScribe will automatically generate a commit message based on your staged changes.

If you want to set up the hook manually, you can create a file named `prepare-commit-msg` in the `.git/hooks/` directory with the following content:

```bash
#!/bin/sh
zithScribe-prepare-commit-msg "$1"
```

Make sure to make the file executable (`chmod +x .git/hooks/prepare-commit-msg`).

## Development

To set up the development environment:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gitAutoDescribe.git
   cd gitAutoDescribe
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

## Running Tests

To run the unit tests:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

This project uses the Anthropic API for generating commit messages.