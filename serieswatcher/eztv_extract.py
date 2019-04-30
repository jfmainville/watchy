import os
import time
import re
import fnmatch
import glob
from itertools import groupby
import subprocess
from selenium import webdriver


def eztv_extract(show):
    chrome_path = r'/usr/bin/chromedriver'
    url = "https://eztv.ag"
    tv_shows_path = "/mnt/plexdata/TV Shows"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    chrome = webdriver.Chrome(
        executable_path=chrome_path, chrome_options=options)
    site_episodes = []
    filtered_episodes = []
    updated_episodes = []
    final_episodes = []
    show_name = show.split(";")[0]
    show_season = show.split(";")[1]
    search_query = show_name.replace(" ", "-")
    chrome.get(url + "/search/" + search_query)
    time.sleep(5)

    count = len(show_name) + 7
    episodes = chrome.find_elements_by_class_name("forum_thread_post")
    magnets = chrome.find_elements_by_class_name("magnet")

    show_directory = os.path.join(tv_shows_path, show_name)
    if not os.path.exists(show_directory):
        os.makedirs(show_directory)
        os.chmod(show_directory, 0o775)

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
                updated_episodes.append([filtered_episode, link])
                final_episodes = [max(g, key=lambda x: x[0]) for _, g in
                                  groupby(sorted(updated_episodes), lambda x: x[0])]
    return episodes, magnets
