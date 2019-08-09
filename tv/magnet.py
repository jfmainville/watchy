import subprocess
import json


def download_magnet_link(download_tv_show, tv_shows_download_directory):
    # Download the TV show using the magnet link
    try:
        if download_tv_show["seeds"] >= 5:
            subprocess.check_output(
                ["aria2c", "-d", tv_shows_download_directory, "--bt-stop-timeout=900", "--seed-time=0", download_tv_show["magnet"]])
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


download_tv_show = {'name': 'Last Week Tonight With John Oliver S06E14', 'seeds': 30,
                    'magnet': 'magnet:?xt=urn:btih:06fe9d2b2e08ac20ebb61a0d896cc842bbf2f949&dn=Last.Week.Tonight.With.John.Oliver.S06E14.HDTV.x264-UAV%5Beztv%5D&tr=udp://tracker.coppersurfer.tk:80&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.leechers-paradise.org:6969&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://exodus.desync.com:6969'}
download_magnet_link(download_tv_show=download_tv_show,
                     tv_shows_download_directory="/app/watch/downloads/tv")
