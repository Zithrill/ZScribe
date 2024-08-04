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
3. Provide a more detailed description in the body, explaining what changes were made and why.
4. Wrap the body at 72 characters.
5. Use bullet points for multiple changes if necessary.


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
3. Is clear, concise, and informative.


Assistant:"""

    response = client.completions.create(
        prompt=prompt,
        max_tokens_to_sample=500,
        model="claude-2.0",
        temperature=0.5,
        top_p=1,
    )

    return response.completion.strip()