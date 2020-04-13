import time
import re
from selenium import webdriver


def leet_extract_movies(movie_title):
    # Extract the movies list from the 1337x site
    chrome_path = r'/usr/lib/chromium/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome = webdriver.Chrome(
        executable_path=chrome_path, chrome_options=options)

    # Navigate to the 1337x site and execute a search sorted search based on the number of seeds
    leet_url = "https://1337x.to"
    encoded_movie_title = movie_title.replace(" ", "%20")
    chrome.get(leet_url + "/sort-search/" +
               encoded_movie_title + "/seeders/desc/1/")
    time.sleep(5)

    leet_movie_torrents = chrome.find_elements_by_class_name("name")
    # 1337x torrent movies list
    leet_movies_list = []
    # Create a list of all the torrent movies
    for leet_movie_torrent in leet_movie_torrents:
        for leet_movie_torrent_name in leet_movie_torrent.get_attribute("innerText").split("\n"):
            # Cleanup the movie title string before comparison
            clean_movie_title = re.sub('[^A-Za-z0-9]+', ' ', movie_title).lower()
            clean_leet_movie_torrent_name = re.sub('[^A-Za-z0-9]+', ' ', leet_movie_torrent_name).lower()
            if clean_movie_title in clean_leet_movie_torrent_name:
                leet_movies_list.append(leet_movie_torrent_name)
    # Extract the full URL of the torrent with the most seeds
    torrent_link = chrome.find_element_by_partial_link_text(
        leet_movies_list[0]).get_attribute("href")
    # Navigate to the torrent page
    chrome.get(torrent_link)
    time.sleep(5)
    # Extract the number of seeds from the torrent page
    seeds = chrome.find_elements_by_class_name(
        "seeds")[0].get_attribute("innerText")
    # Extract the magnet link from the torrent page
    magnet_link = chrome.find_element_by_css_selector(
        '[href^=magnet]').get_attribute("href")
    chrome.quit()
    return seeds, magnet_link
