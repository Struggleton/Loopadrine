import subprocess
import glob
import re
import os
import argparse

# Constants for paths
PROCESSED_DIR = "./~processed/"
DOWNLOADS_DIR = "./~downloads/"
OUTPUT_DIR = "./~output/"
REDO_DIR = "./~redo/"

LOOP_OUTPUT_DIR = os.path.join(DOWNLOADS_DIR, "LooperOutput/")

TOOLS_LOOPINGAUDIO_DIR = "Tools/LoopingAudioConverter/"
TOOLS_YTDLP = "Tools/yt-dlp/"

LOOP_FILENAME = "loop.txt"
SONG_LIST = "songs.txt"
MUSIC_INPUT_EXT = ".wav"
MUSIC_OUTPUT_EXT = ".brstm"

def verify_workspace():
    directories = [PROCESSED_DIR, DOWNLOADS_DIR, OUTPUT_DIR, REDO_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)


def get_sanitized_music_names(music_files):
    # Create a list of names to return after
    # removing all non-ascii characters
    sanitized_music_names = []
    for music_file in music_files:
        # Strip the file name using Regex and
        # the char's hex code
        sanitized_name = re.sub(r"[^\x00-\x7f]", r"", music_file)
        sanitized_music_names.append(sanitized_name)

        # Rename files to their sanitized versions
        os.rename(music_file, sanitized_name)
    return sanitized_music_names


def move_files_to_dir(file_ext, source_dir, dest_dir):
    # Join the extension to the source directory so we can search
    # for that file type
    search_list = glob.glob(os.path.join(source_dir, f"*{file_ext}"))
    for file_name in search_list:
        # Create a new file path based on the basename and
        # destination directory
        basename = os.path.basename(file_name)
        dest_file = os.path.join(dest_dir, basename)

        # Move the file to the new directory
        os.replace(file_name, dest_file)


def delete_files_with_extension(directory, extension):
    # Get all files in provided directory
    # If the filename ends with the provided extension, delete it
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Error deleting {filename}: {e}")


def clear_workspace(del_process=True, del_download=True, del_loop=True):
    # Clear the files from the processed, downloads and loopOutput folders
    if del_process:
        delete_files_with_extension(PROCESSED_DIR, MUSIC_INPUT_EXT)
    if del_download:
        delete_files_with_extension(DOWNLOADS_DIR, MUSIC_INPUT_EXT)
    if del_loop:
        downloads_loop = os.path.join(LOOP_OUTPUT_DIR, LOOP_FILENAME)
        converter_loop = os.path.join(TOOLS_LOOPINGAUDIO_DIR, LOOP_FILENAME)

        if os.path.exists(downloads_loop):
            os.remove(downloads_loop)
        if os.path.exists(converter_loop):
            os.remove(converter_loop)


def download_playlist():
    # Download music from songs.txt to OPUS files
    # using yt-dlp. Use a custom name format
    # to remove the youtube ID from the filename
    download_process = subprocess.run(
        [
            os.path.join(TOOLS_YTDLP, "yt-dlp"),
            "--extract-audio",
            "--audio-format",
            MUSIC_INPUT_EXT[1:],
            "--paths",
            DOWNLOADS_DIR,
            "--batch-file",
            SONG_LIST,
            "-o %(title)s",
        ]
    )


def generate_loops(files, auto_looping):
    # If auto_looping is enabled, add the interactive command
    # tothe arg-list
    export_option = ["export-points"]
    if not auto_looping:
        export_option.insert(0, "-i")
    # Common part of the command
    py_looper_command = ["python", "-m", "pymusiclooper"]

    # Loop over the file names and use pymusiclooper
    # to generate loops. Create a new window
    # so we can avoid any issues with the CTRL+C
    # command.
    for file_name in files:
        subprocess.call(
            py_looper_command
            + export_option
            + ["--path", file_name, "--export-to", "txt"],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

        pretty_name = os.path.basename(file_name)
        print(f"Generated loop point pair for {pretty_name}.")

        # Get the file without a path
        base_name = os.path.split(file_name)[1]

        # Move the file to the processed directory
        new_path = os.path.join(PROCESSED_DIR, base_name)
        os.replace(file_name, new_path)


def generate_brstms(music_names):
    # Get the path for the looping file that should be generated
    loop_file_path = os.path.join(LOOP_OUTPUT_DIR, LOOP_FILENAME)
    if os.path.exists(loop_file_path):
        # Get the path for the new location we should move the loop file to
        looping_audio_file_path = os.path.join(TOOLS_LOOPINGAUDIO_DIR, LOOP_FILENAME)
        os.replace(loop_file_path, looping_audio_file_path)
    # For some reason, LoopingAudioConverter
    # doesn't work if the application is not run
    # from the working directory
    prev_dir = os.path.abspath(os.getcwd())
    os.chdir(TOOLS_LOOPINGAUDIO_DIR)

    # Pass the music path to the LoopingAudioConverter
    for music_file in music_names:
        subprocess.run(f'LoopingAudioConverter --auto "{music_file}"')

        pretty_name = os.path.basename(music_file)
        print(f"Generated looping audio file from {pretty_name}")
    # Go back to the previous directory and
    # move all of the output files to the ~output
    # dir
    os.chdir(prev_dir)

    # Get the directory with all of the BRSTM files and move them
    # up to our ~output directory.
    output_brstm_dir = os.path.join(TOOLS_LOOPINGAUDIO_DIR, "output")
    move_files_to_dir(".brstm", output_brstm_dir, OUTPUT_DIR)


def get_looping_mode():
    # Get whether or not to use interactive loop searching
    auto_looping = True
    while True:
        auto = input(
            "Would you like to use interactive loop generation "
            + "or automatic? (inter/auto) "
        )
        if auto == "inter":
            auto_looping = False
            break
        elif auto == "auto":
            break
    return auto_looping


def main():
    # Ensure we have required folders
    verify_workspace()

    # Set up an argument parser to check if we should redo song loop generation
    # and or skip loop file creation
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--redo", action="store_true", help="Redo song loops")
    parser.add_argument(
        "-s", "--skip", action="store_true", help="Skip generating loop file"
    )

    args = parser.parse_args()

    if args.redo == True:
        input(
            "Make sure the brstm(s) you'd like to re-loop are in the ~redo "
            + "folder and the corresponding opus file is in the ~processed folder. "
            + "Press enter to continue. "
        )

        # Gather the brstm files to redo
        redo_files = glob.glob(os.path.join(REDO_DIR, f"*{MUSIC_OUTPUT_EXT}"))
        for redo_file in redo_files:
            # Move their corresponding opus file back to the download
            # directory so it can be relooped
            base_name = os.path.splitext(os.path.basename(redo_file))[0]
            music_file = base_name + MUSIC_INPUT_EXT

            processed_file_path = os.path.join(PROCESSED_DIR, music_file)
            if os.path.exists(processed_file_path):
                download_file_path = os.path.join(DOWNLOADS_DIR, music_file)
                os.replace(processed_file_path, download_file_path)
        # Clear the current loop file so it can be regenerated
        # If the argument to skip regenerating it is set, don't
        # delete it.
        clear_workspace(del_process=False, del_download=False, del_loop=not args.skip)
    # If we're not redoing the loops, clear the workspace
    # and download more music.
    else:
        clear_workspace()
        download_playlist()
    # Gather all of the downloaded opus files and remove any non-ascii chars
    music_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"*{MUSIC_INPUT_EXT}"))
    sanitized_music_names = get_sanitized_music_names(music_files)

    # If there are no files to process, stop executing
    if (len(sanitized_music_names) <= 0):
        print("There are no files to process!")
        return

    # Generate a looping file if the argument isn't set
    if args.skip == False:
        # Get whether or not to use auto looping or interactive
        auto_looping = get_looping_mode()
        generate_loops(sanitized_music_names, auto_looping)
    else:
        # We move files during the loop generation process to the
        # ~processed folder. Just move all of the files over because
        # we don't need to generate the loop.
        move_files_to_dir(".opus", DOWNLOADS_DIR, PROCESSED_DIR)
    # Get new absolute paths for each song
    new_song_paths = [
        os.path.abspath(os.path.join(PROCESSED_DIR, os.path.basename(song)))
        for song in sanitized_music_names
    ]

    # Create the BRSTMs from the list of opus files
    generate_brstms(new_song_paths)


if __name__ == "__main__":
    main()
