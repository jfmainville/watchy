import subprocess
import logging

logger = logging.getLogger(__name__)


def download_magnet_link(download_entry, download_directory):
    # Download the TV show using the magnet link
    try:
        # Download only torrents that have 5 seeds or more
        if download_entry["seeds"] >= 5:
            logger.info("starting download for %s", download_entry["title"])
            subprocess.check_output(
                ["aria2c", "-d", download_directory, "--bt-stop-timeout=3500", "--seed-time=0",
                 download_entry["magnet"]], timeout=3600)
            return_code = 0
            logger.info("completed download for {0} (return_code={1})".format(download_entry["title"], return_code))
            return return_code
        else:
            # Return code 7 if the amount of seeds is below 5
            return_code = 7
            logger.info("less than 5 seeds for {0} (return_code={1})".format(download_entry["title"], return_code))
            return return_code
    except subprocess.CalledProcessError as error:
        # Return code 7 if the aria2c command line application crashes
        if error.returncode == 7:
            return_code = 7
            logger.error(
                "aria2c command crashed during execution for {0} (return_code={1})".format(download_entry["title"],
                                                                                           return_code))
            return return_code
    except subprocess.TimeoutExpired as error:
        # Return code 2 if the aria2c command timeout
        return_code = 2
        logger.error("aria2c command timeout during execution for {0} (return_code={1})".format(download_entry["title"],
                                                                                                return_code))
        return return_code
