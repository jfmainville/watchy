import subprocess
import json


def download_magnet_link(download_movie, movies_download_directory):
    # Download the movie using the magnet link
    try:
        # Download only torrents that have 5 seeds or more
        if download_movie["seeds"] >= 5:
            subprocess.check_output(
                ["aria2c", "-d", movies_download_directory, "--bt-stop-timeout=300", "--seed-time=0", download_movie["magnet"]], timeout=1800)
            returncode = 0
            return returncode
        else:
            # Return code 7 if the amount of seeds is below 5
            returncode = 7
            return returncode
    except subprocess.CalledProcessError as error:
        # Return code 7 if the aria2c command line application crashes
        if error.returncode == 7:
            returncode = 7
            return returncode
    except subprocess.TimeoutExpired as error:
        # Return code 2 if the aria2c command timeout
        returncode = 2
        return returncode