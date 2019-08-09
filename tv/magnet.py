import subprocess
import json


def download_magnet_link(download_tv_show, tv_shows_download_directory):
    # Download the TV show using the magnet link
    try:
        if download_tv_show["seeds"] >= 5:
            subprocess.check_output(
                ["aria2c", "-d", tv_shows_download_directory, "--bt-stop-timeout=300", "--seed-time=0", download_tv_show["magnet"]])
            returncode = 0
            return returncode
        else:
            returncode = 7
            return returncode
    except subprocess.CalledProcessError as error:
        # If a timeout occurs, create an empty file to prevent future downloads
        if error.returncode == 7:
            returncode = 7
            return returncode
