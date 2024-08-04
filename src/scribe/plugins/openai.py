# src/scribe/plugins/openai.py

import os
from typing import List
import openai

class OpenAIPlugin:
    def __init__(self, model: str):
        self.model = model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            self._client = openai.OpenAI(api_key=api_key)
        return self._client

    @classmethod
    def supported_models(cls) -> List[str]:
        return cls.list_models()

    @classmethod
    def list_models(cls) -> List[str]:
        # Return a static list of models
        return ["gpt-3.5-turbo", "gpt-4"]

    def generate_commit_message(self, diff_summary: str) -> str:
        prompt = f"""As an AI assistant specialized in generating git commit messages, your task is to create a concise and informative commit message based on the following git diff summary:

{diff_summary}

Please follow these guidelines:
1. Start with a subject line no longer than 50 characters, using the imperative mood.
2. Leave a blank line after the subject line.
3. Provide a more detailed description in the body, explaining what changes were made and why.
4. Wrap the body at 72 characters.
5. Use bullet points for multiple changes if necessary.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates git commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    def refine_commit_message(self, message: str, diff_summary: str) -> str:
        prompt = f"""You are an AI assistant specialized in refining git commit messages. You've been given the following commit message:

{message}

And the original diff summary:

{diff_summary}

Please refine the commit message to ensure it:
1. Accurately reflects the changes in the diff summary.
2. Follows the commit message best practices (50 char subject line, detailed body, etc.).
3. Is clear, concise, and informative.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that refines git commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()

    def generate_pull_request_message(self, diff_summary: str, commit_messages: List[str]) -> str:
        formatted_commit_messages = "\n".join(commit_messages)

        prompt = f"""As an AI assistant specialized in generating pull request descriptions, your task is to create a comprehensive and informative message based on the following information:

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
8. Use markdown formatting for better readability.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates pull request descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
