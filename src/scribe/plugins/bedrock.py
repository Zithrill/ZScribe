# src/scribe/plugins/bedrock.py

import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoRegionError, NoCredentialsError, NoAuthTokenError
from typing import List
from .base import BasePlugin


class BedrockPlugin(BasePlugin):
    def __init__(self, model: str):
        self.provider = "Bedrock"
        self.model = model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            try:
                self._client = boto3.client('bedrock-runtime')
            except (NoRegionError, NoCredentialsError, NoAuthTokenError) as e:
                print("Please review README for setting up AWS Bedrock runtime")
                raise e

        return self._client

    @classmethod
    def supported_models(cls) -> List[str]:
        return cls.list_models()

    @classmethod
    def list_models(cls) -> List[str]:
        try:
            bedrock = boto3.client('bedrock')
            response = bedrock.list_foundation_models()
            models = [model['modelId'] for model in response['modelSummaries']]
            return models
        except BotoCoreError:
            return []

    def _invoke_model(self, prompt: str) -> str:
        if self.model not in self.supported_models():
            raise ValueError(f"Unsupported Bedrock model: {self.model}. Supported models are: {', '.join(self.supported_models())}")

        try:
            body = json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
                "top_p": 1,
            })
            response = self.client.invoke_model(
                body=body,
                modelId=self.model,
                accept='application/json',
                contentType='application/json'
            )
            response_body = json.loads(response.get('body').read())
            return response_body.get('completion', '').strip()
        except ClientError as e:
            raise RuntimeError(f"Bedrock API error: {str(e)}")

    def generate_commit_message(self, diff_summary: str) -> str:
        prompt = f"""As an AI assistant specialized in generating git commit messages, create a concise and informative commit message based on the following git diff summary:

{diff_summary}

Please follow these guidelines:
1. Start with a subject line no longer than 50 characters, using the imperative mood.
2. Leave a blank line after the subject line.
3. Provide a more detailed description in the body, explaining what changes were made and why.
4. Wrap the body at 72 characters.
5. Use bullet points for multiple changes if necessary.

Generate the commit message:"""

        return self._invoke_model(prompt)

    def refine_commit_message(self, message: str, diff_summary: str) -> str:
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

        return self._invoke_model(prompt)

    def generate_pull_request_message(self, diff_summary: str, commit_messages: List[str]) -> str:
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

        return self._invoke_model(prompt)
