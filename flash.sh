#!/bin/bash

wait_for_page_changes() {
    local current_focus=""
    local new_focus_value=""
    while true; do
        new_focus_value=$(adb -s localhost shell dumpsys window | grep "mCurrentFocus" | awk -F '[=}]' '{print $2}')
        if [[ "$new_focus_value" != "$current_focus" ]]; then
          echo "Page Changed"
          return
        fi
        sleep 0.2
    done
}

# Monitor that PIN input is appear, it's just workarounds
wait_for_pin() {
    while true; do
      if adb -s localhost shell dumpsys window | grep -q "com.shopee.id/com.shopee.app.react.ReactTransparentActivity_"; then
          echo "PIN Page"
          return
      fi
      sleep 0.2 # recheck
    done
}

date_time="$1"
if [ -z "$date_time" ]; then
    echo "Error: Please provide the date-time string."
    exit 1
fi

# For UNIX
#future_seconds=$(date -j -f "%Y-%m-%d %H:%M:%S" "$date_time" +%s 2>/dev/null)
# For Linux
future_seconds=$(date -d "$date_time" +%s 2>/dev/null)

# shellcheck disable=SC2181
if [ $? -ne 0 ]; then
    echo "Error: Invalid date-time format. Please use 'YYYY-MM-DD HH:MM:SS'."
    exit 1
fi

current_seconds=$(date +%s)
remaining_seconds=$((future_seconds - current_seconds))
if [ "$remaining_seconds" -lt 0 ]; then
    echo "Expired"
else
    echo "$remaining_seconds seconds to go"
    sleep "$remaining_seconds"
    echo "Start $(date)"
    start_time=$(date +%s)
    start_time=$((start_time * 1000))

    adb -s localhost input swipe $((16#0000023d)) $((16#00000468)) $((16#0000023d)) $((16#000005e1)) 77
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))
    sleep 1
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))

    wait_for_page_changes
    sleep 2.7
    adb -s localhost shell input tap $((16#0000031e)) $((16#0000089f))

    wait_for_pin
    sleep 1
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 9
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 11
    adb -s localhost shell input keyevent 12
    adb -s localhost shell input keyevent 13

    end_time=$(date +%s)
    end_time=$((end_time * 1000))
    duration=$((end_time - start_time))
    duration=$((duration / 1000))
    echo "Finish $(date) ($duration seconds)"
fi

echo "End Script"

