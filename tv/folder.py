import os
import glob
from fnmatch import fnmatch
from shutil import move, rmtree


def create_tv_show_folders(tv_shows_directory, tv_shows_download_directory, show_name):
    # Create the TV show folder if it doesn't already exists
    tv_show_directory = os.path.join(tv_shows_directory, show_name)
    tv_show_download_directory = os.path.join(tv_shows_download_directory)
    if os.path.isdir(tv_show_directory) is False:
        os.makedirs(tv_show_directory)
    if os.path.isdir(tv_show_download_directory) is False:
        os.makedirs(tv_show_download_directory)


def get_tv_show_folder_episodes(tv_shows_directory, show_name):
    # Get the list of TV show episodes that were already downloaded
    tv_show_directory = os.path.join(tv_shows_directory, show_name)
    os.chdir(tv_show_directory)
    file_extensions = ("*.mp4", "*.avi", "*.mkv", "*.old")
    tv_show_directory_episodes_extension = []
    tv_show_directory_episodes = []
    if os.path.isdir(tv_show_directory):
        # Extract all the files with the required extensions
        for file_extension in file_extensions:
            tv_show_directory_episodes_extension.extend(
                glob.glob(file_extension))
        # Export the episode name only without the extension
        for tv_show_directory_episode_extension in tv_show_directory_episodes_extension:
            split_text = tv_show_directory_episode_extension.split(".")[
                0]
            tv_show_directory_episodes.append(split_text)
    return tv_show_directory_episodes


def move_tv_show_episode(download_tv_show, tv_show_download_directory, tv_shows_directory, show_name, returncode):
    # Move the download file to the TV show directory
    if returncode == 0:
        # Move the episode file to the TV show directory
        file_extensions = ("*.mp4", "*.avi", "*.mkv")
        tv_show_download_file = []
        # Extract all the videos files from the TV shows download directory
        for path, subdirs, files in os.walk(tv_show_download_directory):
            for name in files:
                for file_extension in file_extensions:
                    if fnmatch(name, file_extension):
                        tv_show_file_extension = file_extension.split(".")[1]
                        tv_show_download_file = os.path.join(path, name)
        # Move file only if the correct file is found with the right extension
        if tv_show_download_file != []:
            # Update the file permissions
            os.chmod(path=tv_show_download_file, mode=0o775)
            # Move the TV show file to the TV show directory
            move(src=tv_show_download_file, dst=tv_shows_directory +
                 "/" + show_name + "/" + download_tv_show["name"] + "." + tv_show_file_extension)
            # Remove all the files under the TV shows download directory
            rmtree(path=tv_show_download_directory)
    if returncode > 0:
        # Create an empty file with a movie extension
        open(file=os.path.join(tv_shows_directory, show_name,
                               download_tv_show["name"]) + ".dead", mode='a')
        # Remove all the files under the TV shows download directory
        rmtree(path=tv_show_download_directory)
