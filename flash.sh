#!/bin/bash

# Check if ADB is installed
#if ! command -v adb &> /dev/null; then
#    echo "ADB is not installed. Please install Android SDK Platform-tools."
#    exit 1
#fi

date_time="$1"
if [ -z "$date_time" ]; then
    echo "Error: Please provide the date-time string."
    exit 1
fi

# For UNIX
#future_seconds=$(date -j -f "%Y-%m-%d %H:%M:%S" "$date_time" +%s 2>/dev/null)

# For Linux
future_seconds=$(date -d "$date_time" +%s 2>/dev/null)

# Check if the conversion was successful
# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "Error: Invalid date-time format. Please use 'YYYY-MM-DD HH:MM:SS'."
    exit 1
fi

current_seconds=$(date +%s)

# Convert future_seconds to millis if need
#future_seconds=$((future_seconds * 1000))
#current_seconds=$((current_seconds * 1000))

remaining_seconds=$((future_seconds - current_seconds))
if [ "$remaining_seconds" -lt 0 ]; then
    echo "Expired"
else
    echo "$remaining_seconds seconds to go"
    sleep "$remaining_seconds"
    echo "Start"
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
    sleep 1
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
    sleep 2
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
    sleep 3
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 9
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 12
    adb -s localhost shell input keyevent 13
    echo "Finish"
fi

echo "End Script"

