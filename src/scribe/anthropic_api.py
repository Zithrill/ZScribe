import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def generate_commit_message(diff_summary):
    prompt = f"""Human: As an AI assistant specialized in generating git commit messages, your task is to create a concise and informative commit message based on the following git diff summary:

{diff_summary}

Please follow these guidelines:
1. Start with a subject line no longer than 50 characters, using the imperative mood.
2. Leave a blank line after the subject line.
3. Provide a more detailed description in the body, explaining what changes were made and why, not repetitive.
5. Focus on changes to the files and file names to gain more context.
6. When reviewing changes look for hierarchical information to gain additional context. 
7. Wrap the body at 72 characters.
8. Use bullet points for multiple changes if necessary.


Assistant:"""

    response = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=500,
        model="claude-2.0",
        temperature=0.7,
        top_p=1,
    )

    return response.completion.strip()


def refine_commit_message(message, diff_summary):
    prompt = f"""Human: You are an AI assistant specialized in refining git commit messages. You've been given the following commit message:

{message}

And the original diff summary:

{diff_summary}

Please refine the commit message to ensure it:
1. Accurately reflects the changes in the diff summary.
2. Follows the commit message best practices (50 char subject line, detailed body, etc.).
3. Is clear, concise, and informative, not repetitive.


Assistant:"""

    response = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=500,
        model="claude-2.0",
        temperature=0.5,
        top_p=1,
    )
    return response.completion.strip()

def generate_pull_request_message(diff_summary: str, commit_messages: [str]) -> str:
    formatted_commit_messages = "\n".join(commit_messages)

    prompt = f"""Human: As an AI assistant specialized in generating pull request descriptions, your task is to create a comprehensive and informative message based on the following information:

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


Assistant:"""

    response = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=1000,
        model="claude-2.0",
        temperature=0.7,
        top_p=1,
    )

    return response.completion.strip()
