import os
import requests
from typing import List
from .base import BasePlugin


class OllamaPlugin(BasePlugin):
    def __init__(self, model: str):
        self.provider = "Ollama"
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model

    @classmethod
    def supported_models(cls) -> List[str]:
        return cls.list_models()

    @classmethod
    def list_models(cls) -> List[str]:
        try:
            response = requests.get(
                f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/tags",
                timeout=5,
            )
            response.raise_for_status()
            return [model["name"] for model in response.json()["models"]]
        except requests.RequestException as e:
            print(f"Warning: Failed to fetch Ollama models: {str(e)}")
            return []

    def _generate_response(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        data = {"model": self.model, "prompt": prompt, "stream": False}

        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return str(response.json()["response"].strip())
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")

    def generate_commit_message(self, diff_summary: str) -> str:
        if self.model not in self.supported_models():
            raise ValueError(
                f"Unsupported Ollama model: {self.model}. Supported models are: {', '.join(self.supported_models())}"
            )

        prompt = f"""As an AI assistant specialized in generating git commit messages, create a concise and informative commit message based on the following git diff summary:

{diff_summary}

Please follow these guidelines:
1. Start with a subject line no longer than 50 characters, using the imperative mood.
2. Leave a blank line after the subject line.
3. Provide a more detailed description in the body, explaining what changes were made and why.
4. Wrap the body at 72 characters.
5. Use bullet points for multiple changes if necessary.

Generate the commit message:"""

        return self._generate_response(prompt)

    def refine_commit_message(self, message: str, diff_summary: str) -> str:
        if self.model not in self.supported_models():
            raise ValueError(
                f"Unsupported Ollama model: {self.model}. Supported models are: {', '.join(self.supported_models())}"
            )

        prompt = f"""As an AI assistant specialized in refining git commit messages, refine the following commit message based on the git diff summary:

Commit message:
{message}

Git diff summary:
{diff_summary}

Please ensure the refined message:
1. Accurately reflects the changes in the diff summary.
2. Follows the commit message best practices (50 char subject line, detailed body, etc.).
3. Is clear, concise, and informative.

Generate the refined commit message:"""

        return self._generate_response(prompt)

    def generate_pull_request_message(
        self, diff_summary: str, commit_messages: List[str]
    ) -> str:
        if self.model not in self.supported_models():
            raise ValueError(
                f"Unsupported Ollama model: {self.model}. Supported models are: {', '.join(self.supported_models())}"
            )

        formatted_commit_messages = "\n".join(commit_messages)

        prompt = f"""As an AI assistant specialized in generating pull request descriptions, create a comprehensive and informative pull request description based on the following information:

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

Generate the pull request description:"""

        return self._generate_response(prompt)
