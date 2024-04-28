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
        album_artist = audio.tags.get("TPE2").text[0]
        total_discs = int(audio.tags.get("TPOS").text[0].split('/')[1]) if audio.tags.get("TPOS") else 1
        disc_number = int(audio.tags.get("TPOS").text[0].split('/')[0]) if audio.tags.get("TPOS") else 1
        total_tracks = int(audio.tags.get("TRCK").text[0].split('/')[1])
        track_number = int(audio.tags.get("TRCK").text[0].split('/')[0])
        return title, artist, album, album_artist, total_discs, disc_number, total_tracks, track_number
    except Exception as e:
        print(f'Error reading tags for "{mp3_file}": {e}')
        return None, None, None, None, None, None, None


# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to rename MP3 files
def rename_mp3(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            mp3_file = os.path.join(directory, filename)
            title, artist, album, album_artist, total_discs, disc_number, total_tracks, track_number = get_tag_info(mp3_file)
            if title and artist and album and album_artist:
                artist_normalized = normalize_string(artist)
                album_artist_normalized = normalize_string(album_artist)
                album_normalized = normalize_string(album)
                title_normalized = normalize_string(title)
                artist_folder = os.path.join(directory, album_artist_normalized)
                album_folder = os.path.join(artist_folder, album_normalized)
                create_directory(artist_folder)
                create_directory(album_folder)
                disc_number_string = f"{disc_number:02d}" if total_discs > 1 else ""
                track_number_string = f"{track_number:02d} - " if total_tracks > 1 else ""
                album_string = f" - {album_normalized}" if album_normalized != title_normalized else ""
                new_filename = f"{disc_number_string}{track_number_string}{title_normalized} - {artist_normalized.replace(';',',')}{album_string}.mp3"
                new_filepath = os.path.join(album_folder, new_filename)
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
