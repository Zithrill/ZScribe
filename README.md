# ZScribe 📝🤖

ZScribe is an intelligent tool that leverages AI to automatically generate meaningful commit messages and pull request descriptions. By analyzing git diffs, ZScribe provides concise and informative messages, saving developers time and improving the quality of version control documentation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T211DCA3)


## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
  - [Supported Models and Providers](#supported-models-and-providers)
  - [API Keys and Configuration](#api-keys-and-configuration)
- [Usage](#usage)
  - [Automatic Usage with Git Hooks](#automatic-usage-with-git-hooks)
  - [Manual Usage](#manual-usage)
  - [Managing Models](#managing-models)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install ZScribe, use pip:

```bash
pip install zscribe
```

## Configuration

ZScribe supports multiple AI providers through a plugin system. 

### Supported Models and Providers

| Provider | Models |
|----------|--------|
| OpenAI | `gpt-3.5-turbo`, `gpt-4` |
| Anthropic | `claude-3-5-sonnet-20240620`, `claude-3-haiku-20240307` |
| AWS Bedrock | `anthropic.claude-v2`, `ai21.j2-ultra-v1`, `amazon.titan-text-express-v1` |
| Ollama | `llama2`, `mistral-7b` |

> **Note**: Available models for AWS Bedrock may vary based on your access. Ollama models depend on your local installation.

### API Keys and Configuration

<details>
<summary>OpenAI</summary>

1. Go to [OpenAI's website](https://openai.com/) and sign up or log in.
2. Navigate to the API section and create a new API key.
3. Set the environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
</details>

<details>
<summary>Anthropic</summary>

1. Go to [Anthropic's website](https://www.anthropic.com/) and sign up for API access.
2. Once approved, generate an API key from your account dashboard.
3. Set the environment variable:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```
</details>

<details>
<summary>AWS Bedrock</summary>

1. Sign up for an [AWS account](https://aws.amazon.com/) if you don't have one.
2. Request access to AWS Bedrock in your AWS console.
3. Set up AWS CLI and configure it with your credentials:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID='your-access-key'
   export AWS_SECRET_ACCESS_KEY='your-secret-key'
   export AWS_DEFAULT_REGION='your-preferred-region'
   ```
</details>

<details>
<summary>Ollama</summary>

1. Install Ollama on your local machine following instructions from the [Ollama website](https://ollama.ai/).
2. No API key is required as Ollama runs locally.
</details>

## Usage

ZScribe is designed to work automatically through git hooks, but also provides options for manual usage via the command-line interface.

### Automatic Usage with Git Hooks

Once installed and configured, ZScribe can automatically generate commit messages and pull request descriptions using git hooks.

To set up the git hooks:

```bash
zscribe hooks install --type both --model <your-chosen-model>
```

This will install both commit and pull request hooks, using the specified model for both.

After installation, ZScribe will automatically:
- Generate a commit message when you make a commit (you can edit this message before finalizing the commit)
- Generate a pull request description when you create a new pull request

### Manual Usage

While git hooks provide automatic functionality, you can also use ZScribe manually:

1. Generate a commit message:
   ```bash
   zscribe commit <commit1> <commit2> [--refine]
   ```

2. Generate a pull request description:
   ```bash
   zscribe pr <pr_number>
   ```

3. List available models:
   ```bash
   zscribe models
   ```

> **Note**: For manual invocations, you can use the `ZSCRIBE_MODEL` environment variable to specify the model:
> ```bash
> export ZSCRIBE_MODEL='gpt-4'
> zscribe commit HEAD~1 HEAD
> ```

### Managing Models

It's important to note that the model used by git hooks is separate from the one used for manual invocations. 

- To update the model used by git hooks:
  ```bash
  zscribe hooks update --type {commit|pr|both} --model <new-model>
  ```

- The `ZSCRIBE_MODEL` environment variable is only used for manual invocations and does not affect git hooks.

Always use the command-line interface to update the model for hooks. The `ZSCRIBE_MODEL` environment variable does not affect the model used by git hooks.

## Examples

1. Install git hooks with a specific model:
   ```bash
   zscribe hooks install --type both --model gpt-4
   ```

2. Update the model for the commit hook:
   ```bash
   zscribe hooks update --type commit --model claude-3-5-sonnet-20240620
   ```

3. Manually generate a commit message for the last commit:
   ```bash
   zscribe commit HEAD~1 HEAD
   ```

4. Manually generate a pull request description for PR #42:
   ```bash
   zscribe pr 42
   ```

5. List all available models:
   ```bash
   zscribe models
   ```

6. Manually generate a commit message using a specific model (does not affect git hooks):
   ```bash
   ZSCRIBE_MODEL=gpt-4 zscribe commit HEAD~1 HEAD
   ```

## Contributing

Contributions to ZScribe are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

Please make sure to update tests as appropriate and adhere to the project's coding standards.

---

Made with ❤️ by Zithco. Happy coding! 🚀