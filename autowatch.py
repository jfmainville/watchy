import os
import time
import re
import fnmatch
from selenium import webdriver

# chrome_path = r'C:\Users\jfmainville\Downloads\chromedriver_win32\chromedriver'
chrome_path = r'/usr/local/share/chromedriver'

# VARIABLES
url = "https://eztv.ag"
# shows = [
#     "Last Week Tonight With John Oliver;S05",
#     "Supernatural;S13",
#     "Doctor Who 2005;S11",
#     "The Big Bang Theory;S07",
#     "MasterChef US;S09",
#     "The X Factor UK;S14",
#     "Shark Tank;S09",
#     "Dragons Den CA;S12",
#     "Hells Kitchen US;S17",
#     "Cops;S30",
#     "Young Sheldon;S01",
#     "The Night Manager;S01"
# ]
shows = [
    "The Night Manager;S01"
]
process_timeout = "180"
drive = '/mnt/plexdata'
tv_shows_path = '/mnt/plexdata/TV Shows'
downloads_path = "/mnt/plexdata/Downloads"
file_extensions = ("*.mp4", "*.mkv", "*.avi")
output = ""
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
chrome = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)

for show in shows:
    site_episodes = []
    filtered_episodes = []
    show_name = show.split(";")[0]
    show_season = show.split(";")[1]
    search_query = show_name.replace(" ", "-")
    chrome.get(url + "/search/" + search_query)
    time.sleep(3)

    count = len(show_name) + 7
    episodes = chrome.find_elements_by_class_name("forum_thread_post")

    for episode in episodes:
        data = episode.get_attribute("innerText")
        site_episodes.append(data)
        for site_episode in site_episodes:
            pattern = re.match((show_name + " " + show_season), site_episode)
            if pattern:
                data = pattern.string[0:count]
                filtered_episodes.append(data)
                filtered_episodes = list(sorted(set(filtered_episodes)))
    files = os.listdir(tv_shows_path)
    for file in files:
        for filtered_episode in filtered_episodes:
            if fnmatch.fnmatch(file, filtered_episode):
                print(filtered_episode)

chrome.quit()
