FROM python:3.7.3-alpine3.9
WORKDIR /app/watchy
COPY ./requirements /app/watchy/requirements
COPY ./tmdb /app/watchy/tmdb
COPY ./tv /app/watchy/tv
COPY ./movie /app/watchy/movie
RUN apk add --no-cache aria2 chromium-chromedriver
RUN pip3 install -r ./requirements/production.txt
RUN echo '30 * * * * /usr/bin/python3.7 /app/watchy/tv/main.py' > /etc/crontabs/root
RUN echo '30 * * * * /usr/bin/python3.7 /app/watchy/movie/main.py' > /etc/crontabs/root
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
CMD ["crond", "-f"]
