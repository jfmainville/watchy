import os
import glob


def create_tv_show_folder(tv_shows_directory, show_name):
    # Create the TV show folder if it doesn't already exists
    tv_show_directory = os.path.join(tv_shows_directory, show_name)
    if os.path.isdir(tv_show_directory) is False:
        os.makedirs(tv_show_directory)


def get_tv_show_folder_episodes(tv_shows_directory, show_name):
    # Get the list of TV show episodes that were already downloaded
    tv_show_directory = os.path.join(tv_shows_directory, show_name)
    os.chdir(tv_show_directory)
    file_extensions = ("*.mp4", "*.avi", "*.mkv")
    tv_show_directory_episodes_extension = []
    tv_show_directory_episodes = []
    if os.path.isdir(tv_show_directory):
        # Extract all the files with the required extensions
        for file_extension in file_extensions:
            tv_show_directory_episodes_extension.extend(
                glob.glob(file_extension))
        # Export the episode name only without the extension
        for tv_show_directory_episode_extension in tv_show_directory_episodes_extension:
            split_text = tv_show_directory_episode_extension.split(".")[
                0]
            tv_show_directory_episodes.append(split_text)
    return tv_show_directory_episodes
