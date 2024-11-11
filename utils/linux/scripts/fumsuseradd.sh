#!/bin/bash
if [[ "$1" == "--help" ]]; then
    echo "Usage: $(basename "$0") [options]"
    echo ""
    echo "Options:"
    echo "  --help           Show this help message and exit"
    echo "<username> <full_name> <phone_number>"
    # Add more options descriptions as needed
    exit 0
fi
# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <full_name> <phone_number>"
    exit 1
fi

# Assign the arguments to variables
username="$1"
full_name="$2"
phone_number="$3"

# Generate the comment using the provided full name and phone number
comment="$full_name,,$phone_number,"

# Execute the useradd command
if sudo useradd --no-create-home --shell /bin/false --comment "$comment" "$username"; then
    echo "User : $username Created successfully"
else
    echo "Failed to create user"
fi
