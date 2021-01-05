# Watchy

This repository contains the code required to automatically download the TV Shows and Movies from a TMDB Watchlist.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

The following applications need to be installed on the local computer in order to run the project locally:

| Application | Minimum Version |                                       Link |
| ----------- | :-------------: | -----------------------------------------: |
| Python      |     3.7.3 +     |  [Link](https://www.python.org/downloads/) |
| Docker      |    18.09.2 +    | [Link](https://www.docker.com/get-started) |

### Environment Variables

The following environment variables needs to be set to use this application:

| Name                       | Description                                                                      | Value Example                    |
| -------------------------- | :------------------------------------------------------------------------------- | :------------------------------- |
| EZTV_URL                   |     EZTV URL to use to extract the list of TV shows to download                  | eztv.re                          |
| LEET_URL                   |    LEET URL to use to extract the list of movies that are available              | 1337x.to                         |
| TMDB_API_URL               |    TMDB API URL to use to extract the required data for the movies and TV shows  | api.themoviedb.org               |
| TMDB_USERNAME              |    TMDB username used to login on the TMDB website                               | User1                            |
| TMDB_PASSWORD              |    TMDB password used to login on the TMDB website                               | Password!                        |
| TMDB_API_KEY               |    TMDB API key information                                                      | abcdefghijklmnopqrstuvwxyz123456 |
| TMDB_ACCOUNT_ID            |    TMDB account ID used to extract the movies and TV shows watchlist information | 1234567                          |
| TV_SHOW_DIRECTORY          |    TV show directory where the video files are located                           | /mnt/plexdata/TV Shows           |
| TV_SHOW_DOWNLOAD_DIRECTORY |    TV show directory where the video files are downloaded                        | /mnt/plexdata/Downloads/tv_shows |
| MOVIE_DIRECTORY            |    Movie directory where the video files are located                             | /mnt/plexdata/Movies             |
| MOVIE_DOWNLOAD_DIRECTORY   |    Movie directory where the video files are downloaded                          | /mnt/plexdata/Downloads/movies   |

### Development

Once you installed all the required prerequisites, you can now proceed with the deployment of the development
environment by completing the following steps:

1. Execute the below command to download the repository to the local machine:

   `git clone https://github.com/jfmainville/watchy.git`

2. Navigate to the directory:

   `cd watchy`

3. You can now run the following command to start the development environment:

   `docker-compose up --build`

4. When the development environment is no longer required, you can execute the below command to shutdown the
   environment:

   `docker-compose down`