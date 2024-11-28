#!/bin/bash

# Check if there is input available
# if [ -t 0 ]; then
#     echo "No input available. Exiting."
#     exit 1
# fi

EMAIL_CONTENT=$(cat)
echo $EMAIL_CONTENT >>/tmp/test/tstlog.log
OTP=$(echo "$EMAIL_CONTENT" | grep -m 1 "^Subject: " | sed 's/^Subject: //' | cut -d: -f2 | tr -d ' ')
EMAIL=$(echo "$EMAIL_CONTENT" | grep -m 1 "^To: " | sed 's/^To: //')
python3 /opt/FUMS/python-script/send-sms.py "$EMAIL" "$OTP"