# Watchy

This repository contains the code required to automatically download the TV Shows and Movies from a TMDB Watchlist.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

The following applications need to be installed on the local computer in order to run the project locally:

| Application | Minimum Version |                                       Link |
| ----------- | :-------------: | -----------------------------------------: |
| Python      |    3.10.12 +    |  [Link](https://www.python.org/downloads/) |
| Docker      |    24.0.5 +     | [Link](https://www.docker.com/get-started) |

### Environment Variables

The following environment variables needs to be set to use this application:

| Name                       | Description                                                                   | Example                          |
| -------------------------- | :---------------------------------------------------------------------------- | :------------------------------- |
| EZTV_URL                   | EZTV URL to use to extract the list of TV shows to download                   | https://eztv.re                  |
| YTS_URL                    | LEET URL to use to extract the list of movies that are available              | https://yts.lt                   |
| TMDB_API_URL               | TMDB API URL to use to extract the required data for the movies and TV shows  | https://api.themoviedb.org       |
| TMDB_USERNAME              | TMDB username used to login on the TMDB website                               | User1                            |
| TMDB_PASSWORD              | TMDB password used to login on the TMDB website                               | Password!                        |
| TMDB_API_KEY               | TMDB API key information                                                      | abcdefghijklmnopqrstuvwxyz123456 |
| TMDB_ACCOUNT_ID            | TMDB account ID used to extract the movies and TV shows watchlist information | 1234567                          |
| TV_SHOW_DIRECTORY          | TV show directory where the video files are located                           | /mnt/plexdata/TV Shows           |
| TV_SHOW_DOWNLOAD_DIRECTORY | TV show directory where the video files are downloaded                        | /mnt/plexdata/Downloads/tv_shows |
| MOVIE_DIRECTORY            | Movie directory where the video files are located                             | /mnt/plexdata/Movies             |
| MOVIE_DOWNLOAD_DIRECTORY   | Movie directory where the video files are downloaded                          | /mnt/plexdata/Downloads/movies   |
| DEBUG_LEVEL                | Debug level necessary (DEBUG, INFO)                                           | INFO                             |
| TV_SHOW_LOG_FILE           | TV show directory where the log file is located                               | /var/log/watchy/tv.log           |
| MOVIE_LOG_FILE             | Movie directory where the log file is located                                 | /var/log/watchy/movie.log        |
| SEEDS_MINIMUM_COUNT        | Minimum amount of seeds required to start the download of the torrent file    | 3                                |
| PROCESS_TIMEOUT            | Process timeout in seconds of the torrent file download command               | 3600                             |
| TORRENT_LISTEN_PORT        | Torrent port to use for the torrent download connection                       | 7777                             |
| TORRENT_DHT_LISTEN_PORT    | Torrent DHT port to use for the torrent download connection                   | 6800                             |
| CONTENT_CLEANUP_DAYS       | Amount of days to wait before the content is deleted                          | 90                               |

### Usage

There are two commands with different arguments that are available to run depending on the TMDB Watchlist type:

| TMDB Watchlist Type | Command                              |
| :------------------ | :----------------------------------- |
| TV Show             | `poetry run python3 main.py --tv`    |
| Movie               | `poetry run python3 main.py --movie` |

### Development

Once you installed all the required prerequisites, you can now proceed with the deployment of the development
environment by completing the following steps:

1. Execute the below command to download the repository to the local machine:

   `git clone https://github.com/jfmainville/watchy.git`

2. Navigate to the directory:

   `cd watchy`

3. You can now run the following command to start the development environment:

```bash
# Execute the below command to  download TV shows from the TMDB Watchlist
poetry run python3 main.py --tv

# Execute the below command to download movies from the TMDB Watchlist
poetry run python3 main.py --movie
```
