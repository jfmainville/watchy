import os
import glob
from fnmatch import fnmatch
from shutil import move, rmtree


def create_movie_folders(movies_directory, movies_download_directory, movie_title):
    # Create the movie folders if they don't already exists
    movie_directory = os.path.join(movies_directory)
    movie_download_directory = os.path.join(movies_download_directory)
    if os.path.isdir(movie_directory) is False:
        os.makedirs(movie_directory)
    if os.path.isdir(movie_download_directory) is False:
        os.makedirs(movie_download_directory)


def get_local_movies(movies_directory, movie_title):
    # Get the list of movies that were already downloaded
    os.chdir(movies_directory)
    file_extensions = ("*.mp4", "*.avi", "*.mkv", "*.timeout", "*.dead")
    movie_extensions = []
    local_movies = []
    if os.path.isdir(movies_directory):
        # Extract all the files with the required extensions
        for file_extension in file_extensions:
            movie_extensions.extend(
                glob.glob(file_extension))
        # Export the episode name only without the extension
        for movie_extension in movie_extensions:
            split_text = movie_extension.split(".")[
                0]
            local_movies.append(split_text)
    return local_movies


def move_local_movie(download_movie, movies_download_directory, movies_directory, movie_title, return_code):
    # Move the download file to the movie directory
    if return_code == 0:
        # Move the episode file to the movies directory
        file_extensions = ("*.mp4", "*.avi", "*.mkv")
        movie_download_files = []
        # Extract all the videos files from the movies download directory
        for path, subdirs, files in os.walk(movies_download_directory):
            for name in files:
                for file_extension in file_extensions:
                    if fnmatch(name, file_extension):
                        movie_file_extension = file_extension.split(".")[1]
                        movie_download_files.append({
                            "path": os.path.join(path, name),
                            "size": os.path.getsize(os.path.join(path, name))
                        })
        # Extract the largest movie file from the list
        movie_download_file = max(movie_download_files, key=lambda d: d['size'])
        # Move file only if the correct file is found with the right extension
        if movie_download_file:
            # Update the file permissions
            os.chmod(path=movie_download_file["path"], mode=0o775)
            # Move the movie file to the movie directory
            move(src=movie_download_file["path"], dst=movies_directory + "/" +
                                                      download_movie["title"] + "." + movie_file_extension)
            # Remove all the files under the movies download directory
            rmtree(path=movies_download_directory, ignore_errors=True)
    if return_code == 2:
        # Create an empty file with the *.timeout extension if the torrent took too long to download
        open(file=os.path.join(movies_directory,
                               download_movie["title"]) + ".timeout", mode='a')
        # Remove all the files under the movies download directory
        rmtree(path=movies_download_directory, ignore_errors=True)
    if return_code == 7:
        # Create an empty file with the *.dead extension if the movie torrent is unavailable
        open(file=os.path.join(movies_directory,
                               download_movie["title"]) + ".dead", mode='a')
        # Remove all the files under the movies download directory
        rmtree(path=movies_download_directory, ignore_errors=True)
