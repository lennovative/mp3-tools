import os
import shutil
import sys

def flatten_folder(base_dir):
    for root, _, files in os.walk(base_dir):
        if root == base_dir:
            continue  # Skip the base directory itself
        for file in files:
            source = os.path.join(root, file)
            destination = os.path.join(base_dir, file)

            if os.path.exists(destination):
                print(f"Skipping {file}, already exists in base directory.")
                continue

            try:
                shutil.move(source, destination)
                print(f"Moved {file} to base directory.")
            except Exception as e:
                print(f"Error moving {file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python flatten_folder.py <path/to/folder>")
        sys.exit(1)
    base_folder = sys.argv[1]
    if not os.path.exists(base_folder):
        print("The specified folder does not exist.")
        sys.exit(1)
    flatten_folder(base_folder)

