FROM ubuntu:20.04
WORKDIR /app/watchy
COPY ./requirements /app/watchy/requirements
COPY ./watchy /app/watchy/watchy
ENV TIMEZONE=America/New_York
RUN ln -snf /usr/share/zoneinfo/TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --quiet --assume-yes python3-pip aria2 cron curl unzip
RUN pip3 install -r ./requirements/dev.txt
RUN mkdir -p "/mnt/plexdata/TV Shows"
RUN mkdir -p "/mnt/plexdata/Downloads/tv_shows"
RUN mkdir -p "/mnt/plexdata/Movies"
RUN mkdir -p "/mnt/plexdata/Downloads/movies"
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
CMD cron -f