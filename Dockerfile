FROM ubuntu:16.04
ADD . /usr/local/bin/autowatch
ADD chromedriver /usr/local/share/chromedriver
RUN chmod +x /usr/local/share/chromedriver
ADD autowatch-cron /etc/cron.d/autowatch-cron
RUN chmod +x /etc/cron.d/autowatch-cron
RUN touch /var/log/autowatch.log
WORKDIR /usr/local/bin/autowatch
RUN apt-get update && apt-get install software-properties-common python-software-properties cron transmission-cli chromium-browser -y
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install python3.6 python3-pip -y && python3.6 -m pip install -r requirements/production.txt && python3.6 -m pip install --upgrade pip
RUN /usr/bin/crontab /etc/cron.d/autowatch-cron
CMD cron && tail -f /var/log/autowatch.log

