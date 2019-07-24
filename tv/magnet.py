import subprocess
import json


def download_magnet_link(download_tv_show, tv_shows_download_directory):
    subprocess.check_output(
        ["aria2c", "-d", tv_shows_download_directory, "--seed-time=0", download_tv_show])
