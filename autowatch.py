#!/usr/bin/env python

import os
import time
import re
import fnmatch
import glob
import pandas as pd
import subprocess
from selenium import webdriver


chrome_path = r'/usr/local/share/chromedriver'
url = "https://eztv.ag"
shows = [
    "Last Week Tonight With John Oliver;S05",
    "Supernatural;S13",
    "Doctor Who 2005;S11",
    "The Big Bang Theory;S07",
    "MasterChef US;S09",
    "The X Factor UK;S15",
    "Shark Tank;S10",
    "Dragons Den CA;S13",
    "Hells Kitchen US;S17",
    "Young Sheldon;S02",
    "The Night Manager;S01"
]
process_timeout = "180"
drive = "/mnt/plexdata"
tv_shows_path = "/mnt/plexdata/TV Shows"
downloads_path = "/mnt/plexdata/Downloads"
cleanup_script_path = "/mnt/plexdata/Scripts/cleanup.sh"
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
chrome = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)


for show in shows:
    site_episodes = []
    filtered_episodes = []
    final_episodes = []
    show_name = show.split(";")[0]
    show_season = show.split(";")[1]
    search_query = show_name.replace(" ", "-")
    chrome.get(url + "/search/" + search_query)
    time.sleep(5)

    count = len(show_name) + 7
    episodes = chrome.find_elements_by_class_name("forum_thread_post")
    magnets = chrome.find_elements_by_class_name("magnet")

    for episode in episodes:
        data = episode.get_attribute("innerText")
        site_episodes.append(data)
        for site_episode in site_episodes:
            pattern = re.match((show_name + " " + show_season), site_episode)
            if pattern:
                data = pattern.string[0:count]
                filtered_episodes.append(data)
                filtered_episodes = list(sorted(set(filtered_episodes)))
    for directory in os.walk(tv_shows_path):
        for file_path in glob.glob(os.path.join(directory[0], '*.*')):
            file_name = (os.path.split(file_path)[1])
            for filtered_episode in filtered_episodes:
                if fnmatch.fnmatch(file_name, filtered_episode + '*.*'):
                    filtered_episodes.remove(filtered_episode)
    for magnet in magnets:
        for filtered_episode in filtered_episodes:
            modified_episode = filtered_episode.replace(" ", ".")
            link = magnet.get_attribute("Href")
            if re.search(modified_episode, link):
                final_episodes.append([filtered_episode, link])
                data_frame = pd.DataFrame(final_episodes)
                data_frame = data_frame.drop_duplicates([0], keep='first')
                final_episodes = data_frame.values.tolist()
    for final_episode in final_episodes:
        subprocess.call(
            ["transmission-cli", "-w", downloads_path, "-f", cleanup_script_path, final_episode[1]])
        time.sleep(3)
        for root, directories, files in os.walk(downloads_path):
            for file in files:
                source_file_path = os.path.split(os.path.join(root, file))[0]
                file_name = os.path.split(os.path.join(root, file))[1]
                if re.findall("^(?!sample).*", file_name):
                    file_extension = os.path.splitext(file_name)[1]
                    os.rename(source_file_path + "/" + file_name,
                              tv_shows_path + "/" + show_name + "/" + final_episode[0] + file_extension)

chrome.quit()
