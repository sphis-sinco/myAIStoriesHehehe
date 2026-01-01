# === CHANGELOG ===
# v1.2
# - Added external JSON config file for soft configuration
# - Made markdown extensions configurable
# - Made header detection configurable
# - Added configurable prompts and messages
# - Optional file sorting via config
# =================

import os
import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_markdown_files(directory, config):
    files = [
        f for f in os.listdir(directory)
        if any(f.lower().endswith(ext) for ext in config["markdown_extensions"])
        and os.path.isfile(os.path.join(directory, f))
    ]
    return sorted(files) if config["sort_files"] else files

def display_file_list(files):
    for i, f in enumerate(files, start=1):
        print(f"[{i}] : {f}")

def is_header(line, config):
    if not line.lstrip().startswith(config["header_prefix"]):
        return False

    if config["require_space_after_header"]:
        prefix_len = len(config["header_prefix"])
        return line.lstrip().startswith(config["header_prefix"] + " ")

    return True

def read_markdown_sections(filepath, config):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sections = []
    current_section = []

    for line in lines:
        if is_header(line, config):
            if current_section:
                sections.append("".join(current_section))
                current_section = []
        current_section.append(line)

    if current_section:
        sections.append("".join(current_section))

    return sections

def get_valid_directory(config):
    while True:
        directory = input(config["directory_prompt"] + "\n> ").strip()
        if os.path.isdir(directory):
            return directory
        print("Invalid directory.\n")

def confirm_next(config):
    while True:
        resp = input(config["confirm_prompt"]).strip()
        if config["allow_uppercase_confirm"]:
            resp = resp.lower()
        if resp in ("y", "n"):
            return resp == "y"

def main():
    config = load_config()
    directory = get_valid_directory(config)

    while True:
        md_files = get_markdown_files(directory, config)

        if not md_files:
            print("No markdown files found.\n")
            continue

        display_file_list(md_files)

        choice = input("Enter the number of the file to read: ").strip()

        if not choice.isdigit():
            print("Invalid input.\n")
            continue

        index = int(choice) - 1

        if index < 0 or index >= len(md_files):
            print("Number out of range.\n")
            continue

        filepath = os.path.join(directory, md_files[index])
        sections = read_markdown_sections(filepath, config)

        for section in sections:
            print("\n" + section)
            if not confirm_next(config):
                break

        print("\n" + config["restart_message"] + "\n")

main()
