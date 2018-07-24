FROM ubuntu:16.04
ADD . /usr/local/bin/autowatch
ADD chromedriver /usr/local/share/chromedriver
RUN chmod +x /usr/local/share/chromedriver
ADD autowatch-cron /etc/cron.d/autowatch-cron
RUN chmod +x /etc/cron.d/autowatch-cron
RUN touch /var/log/autowatch.log
WORKDIR /usr/local/bin/autowatch
RUN apt-get update && apt-get install software-properties-common python-software-properties cron transmission-cli chromium-browser openssh-server -y
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install python3.6 python3-pip -y && python3.6 -m pip install -r requirements/production.txt && python3.6 -m pip install --upgrade pip
RUN mkdir /var/run/sshd
RUN echo 'root:testssh' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
EXPOSE 22
RUN /usr/bin/crontab /etc/cron.d/autowatch-cron
RUN echo "net.core.rmem_max = 4194304" >> /etc/sysctl.conf
RUN echo "net.core.wmem_max = 1048576" >> /etc/sysctl.conf
CMD ["/usr/sbin/sshd", "-D"]

