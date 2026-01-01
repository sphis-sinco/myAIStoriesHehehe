import os

def get_markdown_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(".md") and os.path.isfile(os.path.join(directory, f))]

def display_file_list(files):
    for i, f in enumerate(files, start=1):
        print(f"[{i}] : {f}")

def read_markdown_sections(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sections = []
    current_section = []

    for line in lines:
        if line.startswith("# "):
            if current_section:
                sections.append("".join(current_section))
                current_section = []
        current_section.append(line)

    if current_section:
        sections.append("".join(current_section))

    return sections

def main():
    directory = input('Please give a [[VALID]] directory\n> ')

    while True:
        md_files = get_markdown_files(directory)

        if not md_files:
            print("No markdown files found.")
            return

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
        sections = read_markdown_sections(filepath)

        for section in sections:
            print(section)
            while True:
                cont = input("Display next section? (y/n): ").strip().lower()
                if cont in ("y", "n"):
                    break
            if cont == "n":
                break

        print("\n--- Restarting file selection ---\n")

main()