# Use a Python image based on Debian
FROM python:3.12.7-bookworm
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# Set work directory
WORKDIR /app

# Install system dependencies (including Postfix)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libdbus-1-dev \
    libsystemd-dev \
    cmake \
    gobject-introspection \
    libgirepository1.0-dev \
    python3-apt \
    cloud-init \
    command-not-found \
    # ubuntu-drivers-common \
    postfix \
    procmail \
    nano \
    ufw \
    # tcpdump \
    # python3-xkit \
    # unattended-upgrades \
    && apt-get clean

# Configure Postfix

COPY ./postfixconf/procmailrc /etc/procmailrc
RUN chmod 644 /etc/procmailrc
RUN   postconf -e "myhostname = automail.fums.ac.ir" && \   
    postconf -e "mydestination = \$myhostname, automail.fums.ac.ir, localhost.fums.ac.ir, localhost" && \
    postconf -e "mailbox_command = /usr/bin/procmail -f- -o /etc/procmailrc"&& \
    postconf -e "maillog_file = /var/log/mail.log"
COPY ./utils/linux/scripts/userdel1 /usr/local/bin/userdel1
RUN chmod +x /usr/local/bin/userdel1
COPY ./postfixconf/postfixlisten.sh /etc/postfix/postfixlisten.sh
# COPY ./postfixconf/main.cf /etc/postfix/main.cf

RUN chmod 755 /etc/postfix/postfixlisten.sh

RUN mkdir -p /opt/FUMS/python-script/
COPY ./postfixconf/send-sms.py /opt/FUMS/python-script/send-sms.py
COPY ./postfixconf/APISMS.py  /opt/FUMS/python-script/APISMS.py
RUN chmod 755 /opt/FUMS/python-script/APISMS.py
RUN chmod 755 /opt/FUMS/python-script/send-sms.py
# Enable Postfix service

RUN service postfix start

RUN mkdir -p /var/log/sms/
RUN mkdir -p /var/log/mail/
RUN touch /var/log/sms/sms.log
RUN touch /var/log/mail/procmail.log

RUN chmod 777 /var/log/sms/sms.log
RUN chmod 777 /var/log/mail/procmail.log
# Copy project dependencies
COPY requirements.txt /app/


RUN pip install --upgrade pip && pip install  -r requirements.txt
# Copy project files
COPY . /app/

WORKDIR /app/
EXPOSE 8000
EXPOSE 25
ENV PATH="/root/.local/bin:$PATH"