import os
import sys
from mutagen.easyid3 import EasyID3


def change_tags_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".mp3"):
                mp3_file = os.path.join(root, filename)
                set_title_to_filename(mp3_file)


def set_title_to_filename(mp3_file):
    try:
        audio = EasyID3(mp3_file)
        filename = os.path.basename(mp3_file)
        title = os.path.splitext(filename)[0]
        audio['title'] = title
        audio.save()
        print(f"Title tag set to filename for {mp3_file}")
    except Exception as e:
        print(f"Error processing {mp3_file} (title): {str(e)}")


def get_dir():
    if len(sys.argv) != 2:
        print("path missing")
        return None
    file_path = sys.argv[1]
    return file_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python {} <path/to/mp3/folder>".format(sys.argv[0]))
        exit()
    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("path does not exist")
        exit()
    change_tags_in_folder(folder_path)
