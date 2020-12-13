FROM ubuntu:20.04
WORKDIR /app/watchy
COPY ./requirements /app/watchy/requirements
COPY ./watchy /app/watchy/watchy
ENV TIMEZONE=America/New_York
RUN ln -snf /usr/share/zoneinfo/TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --quiet --assume-yes python3-pip aria2 cron curl unzip
RUN apt-get update && apt-get install --quiet --assume-yes xvfb libxi6 libgconf-2-4
RUN apt-get update && apt-get install --quiet --assume-yes default-jdk
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install --quiet --assume-yes google-chrome-stable
RUN curl -sS -o ~/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN mv ~/chromedriver /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver
RUN pip3 install -r ./requirements/dev.txt
RUN mkdir /var/log/watchy
RUN touch /var/log/watchy/tv.log
RUN touch /var/log/watchy/movie.log
CMD cron -f