#!/bin/bash

# نمایش راهنمای استفاده
if [[ "$1" == "--help" ]]; then
    echo "Usage: $(basename "$0") [options]"
    echo ""
    echo "Options:"
    echo "  --help           Show this help message and exit"
    echo "  <username> <full_name> <phone_number>   Create a new user"
    echo "  <username> <new_phone_number>  Edit phone number of an existing user"
    exit 0
fi

    username="$1"
    new_phone_number="$2"

    # پیدا کردن کامنت کاربر (شامل شماره تلفن)
    current_comment=$(sudo getent passwd "$username" | cut -d: -f5)

    if [ -z "$current_comment" ]; then
        echo "User $username not found."
        return 1
    fi

    # ویرایش شماره تلفن در کامنت
    new_comment=$(echo "$current_comment" | sed "s/\([^,]*,\)[^,]*\(.*\)/\1$new_phone_number\2/")
    
    # ویرایش کامنت کاربر با استفاده از chfn
    if sudo usermod --comment "$new_comment" "$username"; then
        echo "Phone number for user $username updated successfully."
    else
        echo "Failed to update phone number for user $username."
    fi


# بررسی تعداد آرگومان‌ها
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <username> <full_name> <phone_number>  OR  $0 <username> <new_phone_number>"
    exit 1
fi

