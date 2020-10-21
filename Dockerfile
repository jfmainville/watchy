FROM ubuntu:20.04
WORKDIR /app/watchy
COPY ./requirements /app/watchy/requirements
COPY ./tv /app/watchy/tv
COPY ./movie /app/watchy/movie
ENV TIMEZONE=America/Montreal
RUN ln -snf /usr/share/zoneinfo/TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --quiet --assume-yes python3-pip aria2 chromium-bsu chromium-chromedriver cron
RUN pip3 install -r ./requirements/production.txt
RUN echo '*/30 * * * * python3.7 /app/watchy/tv/main.py' >> /etc/crontabs/root
RUN echo '*/30 * * * * python3.7 /app/watchy/movie/main.py' >> /etc/crontabs/root
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
CMD cron -f
