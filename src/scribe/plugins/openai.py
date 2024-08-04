import os
import openai
from typing import List
from .base import BasePlugin


class OpenAIPlugin(BasePlugin):
    def __init__(self, model: str):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = self.api_key

        self.supported_models = ["gpt-3.5-turbo", "gpt-4"]
        if self.model not in self.supported_models:
            raise ValueError(f"Unsupported OpenAI model: {self.model}. Supported models are: {', '.join(self.supported_models)}")

    def _create_chat_completion(self, messages: List[dict]) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                n=1,
                stop=None,
            )
            return response.choices[0].message['content'].strip()
        except openai.error.OpenAIError as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def generate_commit_message(self, diff_summary: str) -> str:
        messages = [
            {"role": "system", "content": "You are an AI assistant specialized in generating git commit messages."},
            {"role": "user", "content": f"""Create a concise and informative commit message based on the following git diff summary:

{diff_summary}

Please follow these guidelines:
1. Start with a subject line no longer than 50 characters, using the imperative mood.
2. Leave a blank line after the subject line.
3. Provide a more detailed description in the body, explaining what changes were made and why.
4. Wrap the body at 72 characters.
5. Use bullet points for multiple changes if necessary."""}
        ]

        return self._create_chat_completion(messages)

    def refine_commit_message(self, message: str, diff_summary: str) -> str:
        messages = [
            {"role": "system", "content": "You are an AI assistant specialized in refining git commit messages."},
            {"role": "user", "content": f"""Refine the following commit message based on the git diff summary:

Commit message:
{message}

Git diff summary:
{diff_summary}

Please ensure the refined message:
1. Accurately reflects the changes in the diff summary.
2. Follows the commit message best practices (50 char subject line, detailed body, etc.).
3. Is clear, concise, and informative."""}
        ]

        return self._create_chat_completion(messages)

    def generate_pull_request_message(self, diff_summary: str, commit_messages: List[str]) -> str:
        formatted_commit_messages = "\n".join(commit_messages)

        messages = [
            {"role": "system", "content": "You are an AI assistant specialized in generating pull request descriptions."},
            {"role": "user", "content": f"""Create a comprehensive and informative pull request description based on the following information:

Git diff summary:
{diff_summary}

Commit messages:
{formatted_commit_messages}

Please follow these guidelines:
1. Start with a clear and concise title summarizing the main purpose of the pull request.
2. Provide a detailed description of the changes, explaining what was done and why.
3. Highlight any significant changes or new features.
4. Mention any breaking changes or deprecations.
5. If applicable, include any testing or deployment instructions.
6. Include any necessary instructions for testing or reviewing the changes.
7. If applicable, reference any related issues or tickets.
8. Use markdown formatting for better readability."""}
        ]

        return self._create_chat_completion(messages)

# Example usage:
# plugin = OpenAIPlugin("gpt-3.5-turbo")
# commit_message = plugin.generate_commit_message("Files changed: 2\nAdditions: 10\nDeletions: 5\nModified files:\n  - src/main.py\n  - tests/test_main.py")
# print(commit_message)