FROM ubuntu:20.04
WORKDIR /app/watchy
COPY ./requirements /app/watchy/requirements
COPY ./tv /app/watchy/tv
COPY ./movie /app/watchy/movie
RUN apt-get install --quiet aria2 chromium-bsu chromium-chromedriver
RUN pip3 install -r ./requirements/production.txt
RUN echo '*/30 * * * * python3.7 /app/watchy/tv/main.py' >> /etc/crontabs/root
RUN echo '*/30 * * * * python3.7 /app/watchy/movie/main.py' >> /etc/crontabs/root
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
CMD ["crond", "-f"]
