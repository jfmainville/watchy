import subprocess
import json


def download_magnet_link(download_tv_show, tv_shows_download_directory):
    # Download the TV show using the magnet link
    try:
        # Download only torrents that have 5 seeds or more
        if download_tv_show["seeds"] >= 5:
            subprocess.check_output(
                ["aria2c", "-d", tv_shows_download_directory, "--bt-stop-timeout=300", "--seed-time=0",
                 download_tv_show["magnet"]], timeout=600)
            return_code = 0
            return return_code
        else:
            # Return code 7 if the amount of seeds is below 5
            return_code = 7
            return return_code
    except subprocess.CalledProcessError as error:
        # Return code 7 if the aria2c command line application crashes
        if error.return_code == 7:
            return_code = 7
            return return_code
    except subprocess.TimeoutExpired as error:
        # Return code 2 if the aria2c command timeout
        return_code = 2
        return return_code
