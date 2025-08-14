FROM ubuntu:24.04
WORKDIR /app
COPY ./ ./
ENV TIMEZONE=America/New_York
RUN ln -snf /usr/share/zoneinfo/TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --quiet --assume-yes python3-pip aria2 cron curl unzip sudo poetry
RUN pipx install poetry
RUN useradd --create-home titan && echo "titan:titan" | chpasswd && adduser titan sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN mkdir -p "/mnt/plexdata/TV Shows"
RUN mkdir -p "/mnt/plexdata/Downloads/tv_shows"
RUN mkdir -p "/mnt/plexdata/Movies"
RUN mkdir -p "/mnt/plexdata/Downloads/movies"
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
RUN chown -R "titan:titan" /var/log/watchy
USER titan
CMD tail -f /dev/null
