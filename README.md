# ZithScribe

ZithScribe is a command-line tool that automatically generates meaningful commit messages and pull request descriptions using the Anthropic API. By analyzing the differences between git commits, it provides concise and informative messages, saving developers time and improving the quality of version control documentation.

## Installation

To install ZithScribe, you can use pip:

```bash
pip install ZithScribe
```

## Configuration

Before using ZithScribe, make sure to set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Usage

### Managing Git Hooks

ZithScribe uses Git hooks to automatically generate commit messages and pull request descriptions. By default, running the hook management script will install both the commit message and pull request hooks.

To manage the hooks:

```bash
zithScribe-manage-hooks
```

This will install both hooks by default.

To install or remove specific hooks:

- Install only the commit message hook:
  ```
  zithScribe-manage-hooks --install commit
  ```

- Install only the pull request hook:
  ```
  zithScribe-manage-hooks --install pr
  ```

- Remove the commit message hook:
  ```
  zithScribe-manage-hooks --remove commit
  ```

- Remove the pull request hook:
  ```
  zithScribe-manage-hooks --remove pr
  ```

- Remove both hooks:
  ```
  zithScribe-manage-hooks --remove both
  ```

### Generating Commit Messages

Once the commit message hook is installed, ZithScribe will automatically generate a commit message when you run `git commit`. The generated message will be pre-filled in your default editor, where you can review and modify it if necessary.

### Generating Pull Request Descriptions

With the pull request hook installed, ZithScribe will automatically generate a pull request description when you create a new pull request using `git pull-request`. The generated description will be added to your pull request on GitHub.

## Development

To set up the development environment:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ZithScribe.git
   cd ZithScribe
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

This project uses the Anthropic API for generating commit messages and pull request descriptions.