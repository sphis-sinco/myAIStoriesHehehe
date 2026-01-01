# === CHANGELOG ===
# v1.8
# - Added ability to quit the program gracefully by entering 'q' at any prompt
# - Works for directory input, file selection, and post-story confirmation
# =================

import os
import json
import sys

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
    prompt = prompt or config.get("confirm_prompt", "Press 'y' to continue to file selection, 'n' to quit: ")
    while True:
        resp = input(prompt).strip()
        if resp.lower() in ("q", "quit"):
            print("\nExiting program.")
            sys.exit(0)
        if config.get("allow_uppercase_confirm", True):
            resp = resp.lower()
        if resp in ("y", "n"):
            return resp == "y"

def display_story(story_lines):
    print()
    for line in story_lines:
        print(line)
    print()

def read_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_valid_directory(config):
    while True:
        directory = input(config.get("directory_prompt", "Please give a [[VALID]] directory") + "\n> ").strip()
        if directory.lower() in ("q", "quit"):
            print("\nExiting program.")
            sys.exit(0)
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

        choice = input("Enter the number of the file to read (or 'q' to quit): ").strip()
        if choice.lower() in ("q", "quit"):
            print("\nExiting program.")
            sys.exit(0)
        if not choice.isdigit():
            print("Invalid input.\n")
            continue
        index = int(choice) - 1
        if index < 0 or index >= len(json_files):
            print("Number out of range.\n")
            continue

        filepath = os.path.join(directory, json_files[index])
        story_data = read_json_file(filepath)

        print(f"\n# {story_data.get('title', 'Untitled')}")
        print(f"{story_data.get('description', '')}\n")

        story_lines = story_data.get("story", [])
        display_story(story_lines)

        # Wait for confirmation AFTER all lines are displayed
        confirm_next(config)

        print("\n" + config.get("restart_message", "--- Restarting file selection ---") + "\n")

if __name__ == "__main__":
    main()
