import os
import glob
from fnmatch import fnmatch
from shutil import move, rmtree
import logging

logger = logging.getLogger(__name__)


def create_content_folders(content_folder, content_download_folder, content_title):
    # Create the content folders if they don't already exists
    try:
        if content_title is not None:
            content_folder_path = os.path.join(content_folder, content_title)
        else:
            content_folder_path = os.path.join(content_folder)
        content_download_folder_path = os.path.join(content_download_folder)
        if os.path.isdir(content_folder_path) is False:
            os.makedirs(content_folder_path)
        if os.path.isdir(content_download_folder_path) is False:
            os.makedirs(content_download_folder_path)
    except OSError as error:
        logger.error("error while creating the content folders: %s", error)


def get_folder_content(content_folder, content_title):
    # Get the list of content files that were already downloaded
    if content_title is not None:
        content_folder_path = os.path.join(content_folder, content_title)
    else:
        content_folder_path = os.path.join(content_folder)
    os.chdir(content_folder_path)
    file_extensions = ("*.mp4", "*.avi", "*.mkv", "*.timeout", "*.dead")
    content_folder_episodes_extension = []
    content_folder_episodes = []
    if os.path.isdir(content_folder_path):
        # Extract all the files with the required extensions
        for file_extension in file_extensions:
            content_folder_episodes_extension.extend(
                glob.glob(file_extension))
        # Export the content file name only without the extension
        for content_folder_episode_extension in content_folder_episodes_extension:
            split_text = os.path.splitext(content_folder_episode_extension)[0]
            content_folder_episodes.append(split_text)
    return content_folder_episodes


def move_content_file(download_file, content_download_folder, content_folder, content_title, return_code):
    # Move the downloaded file to the content folder
    if return_code == 0:
        # Move the downloaded content file to the content folder
        file_extensions = ("*.mp4", "*.avi", "*.mkv")
        content_download_files = []
        # Extract all the files from the content download folder
        for path, subdirs, files in os.walk(content_download_folder):
            for name in files:
                for file_extension in file_extensions:
                    if fnmatch(name, file_extension):
                        content_file_extension = file_extension.split(".")[1]
                        content_download_files.append({
                            "path": os.path.join(path, name),
                            "size": os.path.getsize(os.path.join(path, name))
                        })
        # Extract the largest content file from the list
        content_download_file = max(content_download_files, key=lambda d: d['size'])
        # Move file only if the correct file is found with the right extension
        if content_download_file:
            # Update the file permissions
            os.chmod(path=content_download_file["path"], mode=0o775)
            # Move the content file to the content folder
            if content_title is not None:
                move(src=content_download_file["path"], dst=content_folder + "/" + content_title + "/" + download_file[
                    "title"] + "." + content_file_extension)
            else:
                move(src=content_download_file["path"],
                     dst=content_folder + "/" + download_file["title"] + "." + content_file_extension)
            # Remove all the files under the content download folder
            rmtree(path=content_download_folder, ignore_errors=True)
    if return_code == 2:
        # Create an empty file with the *.timeout extension if the torrent took too long to download
        if content_title is not None:
            open(file=os.path.join(content_folder, content_title, download_file["title"]) + ".timeout", mode='a')
        else:
            open(file=os.path.join(content_folder, download_file["title"]) + ".timeout", mode='a')
        # Remove all the files under the content download folder
        rmtree(path=content_download_folder, ignore_errors=True)
    if return_code == 7:
        # Create an empty file with the *.dead extension if the content torrent is unavailable
        if content_title is not None:
            open(file=os.path.join(content_folder, content_title, download_file["title"]) + ".dead", mode='a')
        else:
            open(file=os.path.join(content_folder, download_file["title"]) + ".dead", mode='a')
        # Remove all the files under the content download folder
        rmtree(path=content_download_folder, ignore_errors=True)
