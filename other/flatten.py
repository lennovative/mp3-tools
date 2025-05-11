import os
import shutil

def flatten_directory(directory):
    # Iterate over all files and directories in the given directory
    for root, dirs, files in os.walk(directory):
        # Move each file to the base directory
        for file_name in files:
            src = os.path.join(root, file_name)
            dst = os.path.join(directory, file_name)
            shutil.move(src, dst)
            print(f"Moved file: {src} -> {dst}")

    # Delete all subdirectories (including empty ones)
    for dir_name in os.listdir(directory):
        dir_path = os.path.join(directory, dir_name)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            print(f"Deleted directory: {dir_path}")

# Flatten the specified directory
flatten_directory('./')
