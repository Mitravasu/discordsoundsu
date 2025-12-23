#!/bin/bash

# Name your screen session
SESSION_NAME="discordsoundsu"

PROJECT_DIR="/full/path/to/project"

COMMAND="uv run discordsoundsu"  

export PATH=$PATH:/usr/local/bin

# Create a new detached screen session and run commands
screen -dmS $SESSION_NAME bash -c "
cd $PROJECT_DIR
$COMMAND
exec bash"  # keep the screen session alive after command

# reattach with screen -r discordsoundsu

# Run this script on startup
# chmod +x run_discordsoundsu.sh
# crontab -e
# add the following line and save
# @reboot /full/path/to/run_discordsoundsu.sh
