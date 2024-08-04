# ZScribe

ZScribe is a command-line tool that automatically generates meaningful commit messages and pull request descriptions using various AI models. By analyzing the differences between git commits, it provides concise and informative messages, saving developers time and improving the quality of version control documentation.

## Installation

To install ZScribe, you can use pip:

```bash
pip install ZScribe
```

## Configuration

ZScribe supports multiple AI providers through a plugin system. You can configure your preferred model using the `ZSCRIBE_MODEL` environment variable or the `--model` command-line argument.

### Supported Models and Providers

- OpenAI:
  - `gpt-3.5-turbo`
  - `gpt-4`
- Anthropic:
  - `claude-2`
  - `claude-instant-1`
- AWS Bedrock:
  - `anthropic.claude-v2`
  - `ai21.j2-ultra-v1`
  - `amazon.titan-text-express-v1`
  - (Note: Available models may vary based on your AWS Bedrock access)
- Ollama:
  - `llama2`
  - `mistral-7b`
  - (Note: Available models depend on your local Ollama installation)

Example:
```bash
export ZSCRIBE_MODEL='gpt-4'
```

## API Keys and Configuration

### OpenAI

1. Go to [OpenAI's website](https://openai.com/) and sign up or log in.
2. Navigate to the API section and create a new API key.
3. Set the environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

### Anthropic

1. Go to [Anthropic's website](https://www.anthropic.com/) and sign up for API access.
2. Once approved, generate an API key from your account dashboard.
3. Set the environment variable:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

### AWS Bedrock

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

### Ollama

1. Install Ollama on your local machine following instructions from the [Ollama website](https://ollama.ai/).
2. No API key is required as Ollama runs locally.

## Usage

Generate a commit message:
```bash
zscribe commit1 commit2 [--model MODEL_NAME]
```

Generate a pull request description:
```bash
zscribe --pr PR_NUMBER [--model MODEL_NAME]
```

Install git hooks:
```bash
zscribe-manage-hooks [--install {commit,pr,both}] [--model MODEL_NAME]
```

Remove git hooks:
```bash
zscribe-manage-hooks --remove {commit,pr,both}
```

## Dynamic Model Selection

ZScribe now dynamically fetches available models for AWS Bedrock and Ollama. This means:

- For AWS Bedrock: The plugin will list all models available to your AWS account.
- For Ollama: The plugin will list all models installed on your local Ollama instance.

You can view available models by running any ZScribe command with an invalid model name, which will print the list of supported models for the selected provider.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.