import re
from selenium import webdriver


def leet_extract_movies(movie_title, movie_release_year, leet_url):
    # Extract the movies list from the 1337x site
    chromedriver_path = r'/usr/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(
        executable_path=chromedriver_path, chrome_options=options)

    # Navigate to the 1337x site and execute a search sorted search based on the number of seeds
    encoded_movie_title = movie_title.replace(" ", "%20")
    browser.get("https://" + leet_url + "/sort-search/" +
                encoded_movie_title + "%20" + movie_release_year + "/seeders/desc/1/")
    browser.implicitly_wait(5)

    leet_movie_torrents = browser.find_elements_by_class_name("name")

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
    try:
        torrent_link = browser.find_element_by_partial_link_text(
            leet_movies_list[0]).get_attribute("href")

        # Navigate to the torrent page
        browser.get(torrent_link)
        browser.implicitly_wait(5)

        # Extract the number of seeds from the torrent page
        seeds = browser.find_elements_by_class_name(
            "seeds")[0].get_attribute("innerText")

        # Extract the magnet link from the torrent page
        magnet_link = browser.find_element_by_css_selector(
            '[href^=magnet]').get_attribute("href")
        return seeds, magnet_link
    except IndexError:
        seeds = None
        magnet_link = None
        return seeds, magnet_link

    # Close the web browser application
    browser.quit()
