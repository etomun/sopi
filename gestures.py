import subprocess


def capture_touch_events():
    command = ["getevent", "--continuous"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Capture and print the output
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())

    process.terminate()


if __name__ == "__main__":
    capture_touch_events()
