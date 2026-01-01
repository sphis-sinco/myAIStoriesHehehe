# === CHANGELOG ===
# v1.4
# - Switched from markdown files to JSON-based story files
# - Supports nested sections/subsections
# - Reads title, description, and sections from JSON
# - Confirmation system preserved for paging through sections
# =================

import os
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_json_files(directory):
    return sorted(
        f for f in os.listdir(directory)
        if f.lower().endswith(".json") and os.path.isfile(os.path.join(directory, f))
    )

def display_file_list(files):
    for i, f in enumerate(files, start=1):
        print(f"[{i}] : {f}")

def confirm_next(config, prompt=None):
    prompt = prompt or config.get("confirm_prompt", "Display next section? (y/n): ")
    while True:
        resp = input(prompt).strip()
        if config.get("allow_uppercase_confirm", True):
            resp = resp.lower()
        if resp in ("y", "n"):
            return resp == "y"

def display_section(section, config):
    """Recursively display a section and its subsections"""
    print(f"\n=== {section.get('name', 'Unnamed Section')} ===\n")
    for line in section.get("content", []):
        print(line)
    if not confirm_next(config):
        return False

    # Handle subsections recursively
    subsections = section.get("subsections")
    if subsections:
        # if it's a dict (single subsection) or list (multiple)
        if isinstance(subsections, dict):
            subsections = [subsections]
        for sub in subsections:
            if not display_section(sub, config):
                return False
    return True

def read_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_valid_directory(config):
    while True:
        directory = input(config.get("directory_prompt", "Please give a [[VALID]] directory") + "\n> ").strip()
        if os.path.isdir(directory):
            return directory
        print("Invalid directory.\n")

def main():
    config = load_config()
    directory = get_valid_directory(config)

    while True:
        json_files = get_json_files(directory)

        if not json_files:
            print("No JSON story files found.\n")
            continue

        display_file_list(json_files)

        choice = input("Enter the number of the file to read: ").strip()
        if not choice.isdigit():
            print("Invalid input.\n")
            continue
        index = int(choice) - 1
        if index < 0 or index >= len(json_files):
            print("Number out of range.\n")
            continue

        filepath = os.path.join(directory, json_files[index])
        story = read_json_file(filepath)

        print(f"\n# {story.get('title', 'Untitled')}")
        print(f"{story.get('description', '')}\n")

        for section in story.get("sections", []):
            if not display_section(section, config):
                break

        print("\n" + config.get("restart_message", "--- Restarting file selection ---") + "\n")

if __name__ == "__main__":
    main()
