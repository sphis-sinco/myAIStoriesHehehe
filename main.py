# === CHANGELOG ===
# v1.5
# - Removed subsections support; now sections are flat
# - Reads JSON story files with title, description, and flat sections only
# - Confirmation system preserved for paging through each section
# =================

import os
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_json_files(directory, config):
    return sorted(
        f for f in os.listdir(directory)
        if any(f.lower().endswith(ext) for ext in config["story_file_extensions"])
        and os.path.isfile(os.path.join(directory, f))
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
    print(f"\n=== {section.get('name', 'Unnamed Section')} ===\n")
    for line in section.get("content", []):
        print(line)
    return confirm_next(config)

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
        json_files = get_json_files(directory, config)

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
