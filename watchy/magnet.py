import subprocess
import logging

logger = logging.getLogger(__name__)


def download_magnet_link(download_entry, download_directory, seeds_minimum_count, process_timeout, vpn_username,
                         torrent_listen_port, torrent_dht_listen_port):
    # Download the torrent file using the magnet link
    try:
        # Download only torrents that have a certain amount of seeds or more
        if download_entry["seeds"] >= seeds_minimum_count:
            logger.info(
                "starting download for {0} (seeds_count={1})".format(download_entry["title"], download_entry["seeds"]))
            subprocess.check_output(
                ["sudo -u " + vpn_username + " -i --", "aria2c", "-d", download_directory, "--disable-ipv6",
                 "--listen-port", torrent_listen_port, "--listen-dht-port", torrent_dht_listen_port,
                 "--bt-stop-timeout=" + str(process_timeout - 100), "--seed-time=0",
                 download_entry["magnet"]], timeout=process_timeout, shell=True)
            return_code = 0
            logger.info("completed download for {0} (return_code={1})".format(download_entry["title"], return_code))
            return return_code
        else:
            # Return code 7 if the amount of seeds is below than a certain amount
            return_code = 7
            logger.info(
                "less than {0} seeds for {1} (return_code={2})".format(seeds_minimum_count, download_entry["title"],
                                                                       return_code))
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
