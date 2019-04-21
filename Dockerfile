FROM python:3.7.3-alpine3.9
WORKDIR /app/serieswatcher
COPY . /app/serieswatcher
RUN apk add --no-cache aria2 chromium-chromedriver
RUN pip3 install -r requirements.txt
RUN echo '30 * * * * /usr/bin/python3.7 /app/serieswatcher.py' > /etc/crontabs/root
RUN touch /var/log/serieswatcher.log
CMD ["crond", "-f"]
