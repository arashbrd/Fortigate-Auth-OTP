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
    # python3-xkit \
    # unattended-upgrades \
    && apt-get clean

# Configure Postfix
# COPY postfix_main.cf /etc/postfix/main.cf
# RUN postconf -e "myhostname=example.com" \
#     && postconf -e "mydestination=localhost, example.com" \
#     && postconf -e "relayhost=" \
#     && postconf -e "inet_interfaces=all"
COPY ./postfixconf/procmailrc /etc/procmailrc

RUN   postconf -e "myhostname = automail.fums.ac.ir" && \   
    postconf -e "mydestination = \$myhostname, automail.fums.ac.ir, localhost.fums.ac.ir, localhost" && \
    postconf -e "mailbox_command = /usr/bin/procmail -f- -o /etc/procmailrc"

COPY ./postfixconf/postfixlisten.sh /etc/postfix/postfixlisten.sh


RUN chmod +x /etc/postfix/postfixlisten.sh

RUN mkdir -p /opt/FUMS/python-script/
COPY ./postfixconf/send-sms.py /opt/FUMS/python-script/send-sms.py
COPY ./postfixconf/APISMS.py  /opt/FUMS/python-script/APISMS.py

# EXPOSE 25 587
# Enable Postfix service
RUN service postfix start

# Copy project dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install  -r requirements.txt

# Copy project files
COPY . /app/

# Expose ports (Django: 8000, Postfix: 25)
EXPOSE 8000
EXPOSE 25
# RUN systemctl start postfix
# RUN systemctl enable postfix
# Default command to start Django
# CMD ["postfix", "start-fg"]
ENV PATH="/root/.local/bin:$PATH"

#CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
