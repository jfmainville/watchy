import getpass
import time
import datetime
import glob
import logging
import os
import shutil
import subprocess
from fnmatch import fnmatch

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
            os.chmod(path=content_folder_path, mode=0o777)
        if os.path.isdir(content_download_folder_path) is False:
            os.makedirs(content_download_folder_path)
            os.chmod(path=content_download_folder_path, mode=0o777)
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
            content_folder_episodes_extension.extend(glob.glob(file_extension))
        # Export the content file name only without the extension
        for content_folder_episode_extension in content_folder_episodes_extension:
            split_text = os.path.splitext(content_folder_episode_extension)[0]
            content_folder_episodes.append(split_text)
    return content_folder_episodes


def delete_content_download_files(content_download_folder):
    # Delete all the files under the content download folder
    for filename in os.listdir(content_download_folder):
        file_path = os.path.join(content_download_folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def move_content_file(
    download_file, content_download_folder, content_folder, content_title, return_code
):
    # Move the downloaded file to their appropriate content folder
    content_file_extension = None
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
                        content_download_files.append(
                            {
                                "path": os.path.join(path, name),
                                "size": os.path.getsize(os.path.join(path, name)),
                            }
                        )
        # Extract the largest content file from the list
        try:
            content_download_file = max(content_download_files, key=lambda d: d["size"])
        except ValueError:
            error_message = "Unable to move the content as the download directory is empty"
            logger.error(error_message)
            raise ValueError(error_message)
        # Move file only if the correct file is found with the right extension
        if content_download_file:
            # Update the file owner to use the main user
            current_user = getpass.getuser()
            subprocess.check_output(
                "sudo chown -R "
                + current_user
                + ":"
                + current_user
                + " "
                + content_download_folder,
                shell=True,
            )
            # Update the file permissions
            os.chmod(path=content_download_file["path"], mode=0o777)
            # Move the content file to the content folder
            if content_title is not None and content_file_extension is not None:
                # Move the TV show file to the content folder
                destination_path = (
                    os.path.join(content_folder, content_title, download_file["title"])
                    + "."
                    + content_file_extension
                )
                shutil.move(
                    src=content_download_file["path"],
                    dst=content_folder
                    + "/"
                    + content_title
                    + "/"
                    + download_file["title"]
                    + "."
                    + content_file_extension,
                )
            else:
                # Move the movie file to the content folder
                destination_path = (
                    os.path.join(content_folder, download_file["title"])
                    + "."
                    + content_file_extension
                )
                shutil.move(src=content_download_file["path"], dst=destination_path)
            # Remove all the files under the content download folder
            delete_content_download_files(
                content_download_folder=content_download_folder
            )

            return destination_path
    if return_code == 2:
        # Create an empty file with the *.timeout extension if the torrent took too long to download
        if content_title is not None and content_file_extension is not None:
            destination_path = (
                os.path.join(content_folder, content_title, download_file["title"])
                + ".timeout"
            )
            open(file=destination_path, mode="a")
        else:
            destination_path = (
                os.path.join(content_folder, download_file["title"]) + ".timeout"
            )
            open(file=destination_path, mode="a")
        # Remove all the files under the content download folder
        delete_content_download_files(content_download_folder=content_download_folder)

        return destination_path
    if return_code == 7:
        # Create an empty file with the *.dead extension if the content torrent is unavailable
        if content_title is not None:
            destination_path = (
                os.path.join(content_folder, content_title, download_file["title"])
                + ".dead"
            )
            open(file=destination_path, mode="a")
        else:
            destination_path = (
                os.path.join(content_folder, download_file["title"]) + ".dead"
            )
            open(file=destination_path, mode="a")
        # Remove all the files under the content download folder
        delete_content_download_files(content_download_folder=content_download_folder)

        return destination_path


def cleanup_content_folder(content_folder, content_cleanup_days):
    """Cleanup content older than a specific date"""
    os.chdir(content_folder)
    deleted_content_files = []
    today_date = datetime.datetime.now()
    date_delta = today_date - datetime.timedelta(days=int(content_cleanup_days))

    specific_date = time.mktime(
        (date_delta.year, date_delta.month, date_delta.day, 0, 0, 0, 0, 0, 0)
    )
    # List to store the older files
    for path, subdirs, files in os.walk(content_folder):
        for name in files:
            file_path = os.path.join(path, name)
            file_modification_time = os.path.getmtime(file_path)

            # Delete content files that are older than a specific time period
            if file_modification_time < specific_date:
                try:
                    os.remove(file_path)
                    deleted_content_files.append(file_path)
                    logger.info("successfully completed the deletion of the following file: %s", file_path)
                except:
                    logger.error("unable to delete the following file: %s", file_path)
    return deleted_content_files
