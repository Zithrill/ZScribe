import sys
import subprocess
import re


def get_current_version():
    with open("setup.py", "r") as f:
        content = f.read()
    match = re.search(r'version\s*=\s*["\'](.+?)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Version not found in setup.py")


def get_latest_tag_version():
    try:
        latest_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], universal_newlines=True
        ).strip()
        return latest_tag.lstrip("v")
    except subprocess.CalledProcessError:
        return "0.0.0"  # If no tags exist


def compare_versions(current, latest):
    current_parts = list(map(int, current.split(".")))
    latest_parts = list(map(int, latest.split(".")))

    for i in range(max(len(current_parts), len(latest_parts))):
        current_part = current_parts[i] if i < len(current_parts) else 0
        latest_part = latest_parts[i] if i < len(latest_parts) else 0

        if current_part > latest_part:
            return True
        elif current_part < latest_part:
            return False

    return False  # Versions are equal


if __name__ == "__main__":
    current_version = get_current_version()
    latest_tag_version = get_latest_tag_version()

    print(f"Current version: {current_version}")
    print(f"Latest tag version: {latest_tag_version}")

    if compare_versions(current_version, latest_tag_version):
        print("Version has been bumped.")
        sys.exit(0)
    else:
        print("Error: Version has not been bumped.")
        sys.exit(1)
