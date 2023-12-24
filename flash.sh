#!/bin/bash

# Check if ADB is installed
#if ! command -v adb &> /dev/null; then
#    echo "ADB is not installed. Please install Android SDK Platform-tools."
#    exit 1
#fi

adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
adb -s localhost shell input keyevent 11
adb -s localhost shell input keyevent 9
adb -s localhost shell input keyevent 11
adb -s localhost shell input keyevent 11
adb -s localhost shell input keyevent 12
adb -s localhost shell input keyevent 13

