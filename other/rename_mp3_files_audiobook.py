import os
import sys
import unicodedata
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3


# Function to normalize strings to work as filenames
def normalize_string(s):
    # Remove non-ASCII characters
    filename = unicodedata.normalize('NFKD', s)
    filename = ''.join(c for c in filename if not unicodedata.combining(c))
    filename = ''.join(c if ord(c) < 128 else '_' for c in filename)
    # Remove control characters
    filename = ''.join(c for c in filename if unicodedata.category(c)[0] != 'C')
    # Replace characters not allowed in filename
    filename = re.sub(r'[<>\{\}@%&$€#/\\|?!*.]', '_', filename)
    filename = re.sub(r"['\":\[\]]", "", filename)
    filename = re.sub("  ", " ", filename)
    return filename


# Function to get the tag information from MP3 files
def get_tag_info(mp3_file):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        title = audio.tags.get("TIT2").text[0]
        artist = audio.tags.get("TPE1").text[0]
        album = audio.tags.get("TALB").text[0]
        disc_number = int(audio.tags.get("TPOS").text[0].split('/')[0]) if audio.tags.get("TPOS") else 1
        track_number = int(audio.tags.get("TRCK").text[0].split('/')[0])
        return title, artist, album, disc_number, track_number
    except Exception as e:
        print(f'Error reading tags for "{mp3_file}": {e}')
        return None, None, None, None, None


# Function to rename MP3 files
def rename_mp3_old(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_file = os.path.join(directory, filename)
            title, artist, album, disc_number, track_number = get_tag_info(mp3_file)
            if title and artist and album:
                #artist_normalized = normalize_string(artist)
                album_normalized = normalize_string(album)
                #title_normalized = normalize_string(title)
                disc_number_string = f"{disc_number:02d}"
                track_number_string = f"{track_number:02d}"
                new_filename = f"{disc_number_string}{track_number_string} - {album_normalized}.mp3"
                new_filepath = os.path.join(directory, new_filename)
                try:
                    os.renames(mp3_file, new_filepath)
                    print(f'Moved "{filename}" to "{new_filename}"')
                except Exception as e:
                    print(f'Error moving "{filename}": {e}')
            else:
                print(f'Skipping "{filename}" due to missing tag information')


# Function to rename MP3 files in all subdirectories
def rename_mp3(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".mp3"):
                mp3_file = os.path.join(root, filename)
                title, artist, album, disc_number, track_number = get_tag_info(mp3_file)
                if title and artist and album:
                    #artist_normalized = normalize_string(artist)
                    album_normalized = normalize_string(album)
                    #title_normalized = normalize_string(title)
                    disc_number_string = f"{disc_number:02d}"
                    track_number_string = f"{track_number:02d}"
                    new_filename = f"{disc_number_string}{track_number_string}.mp3"
                    new_filepath = os.path.join(root, new_filename)
                    try:
                        os.renames(mp3_file, new_filepath)
                        print(f'Moved "{filename}" to "{new_filename}"')
                    except Exception as e:
                        print(f'Error moving "{filename}": {e}')
                else:
                    print(f'Skipping "{filename}" due to missing tag information')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python {} <path/to/mp3/folder>".format(sys.argv[0]))
        exit()
    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print("path does not exist")
        exit()
    rename_mp3(folder_path)
