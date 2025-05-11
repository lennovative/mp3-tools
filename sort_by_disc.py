import os
import sys
import shutil
from mutagen.easyid3 import EasyID3

def sort_mp3s_by_disc(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            filepath = os.path.join(directory, filename)
            try:
                audio = EasyID3(filepath)
                disc_number_raw = audio.get("discnumber", ["1"])[0]
                disc_number = int(disc_number_raw.split("/")[0])  # Handles '1/2' format
                disc_folder = f"CD{disc_number:02d}"
                destination_folder = os.path.join(directory, disc_folder)

                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(filepath, os.path.join(destination_folder, filename))
                print(f"Moved {filename} to {disc_folder}/")
            except Exception as e:
                print(f"Failed to sort {filename}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort_by_disc.py <path/to/mp3/folder>")
        sys.exit(1)
    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        sys.exit(1)
    sort_mp3s_by_disc(folder_path)

