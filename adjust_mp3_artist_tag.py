import os
import sys
from mutagen.easyid3 import EasyID3


def change_artist_tags_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            mp3_file = os.path.join(folder_path, filename)
            change_artist_tags(mp3_file)


def change_artist_tags(mp3_file):
    try:
        audio = EasyID3(mp3_file)
        if 'artist' in audio:
            artist_string = ";".join(audio['artist'])
            artist_list = artist_string.split(";")
            artist_list = [artist.strip() for artist in artist_list]
            artist_string_final = "; ".join(artist_list)
            audio['artist'] = [artist_string_final]
            audio.save()
            print(f"Artist tags changed successfully for {mp3_file}")
        else:
            print(f"No artist tags found for {mp3_file}")
    except Exception as e:
        print(f"Error processing {mp3_file}: {str(e)}")


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
    change_artist_tags_in_folder(folder_path)
