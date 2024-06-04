import subprocess
import time

def open_new_tab(tab_index):
    cmd = f'start cmd /k "python run.py & exit"'
    print(f"Opening tab {tab_index}")
    subprocess.run(cmd, shell=True)

def close_tabs(tab_handles):
    for handle in tab_handles:
        cmd = f'taskkill /PID {handle} /F'
        print(f"Closing tab with PID {handle}")
        subprocess.run(cmd, shell=True)

def get_cmd_pids():
    result = subprocess.run("tasklist /FI \"IMAGENAME eq cmd.exe\"", shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    lines = output.splitlines()
    pids = []
    for line in lines[3:]:  # Skip the header lines
        parts = line.split()
        if len(parts) >= 2:
            pids.append(parts[1])
    return pids

if __name__ == "__main__":
    tab_handles = []

    for i in range(10):
        open_new_tab(i + 1)
        time.sleep(1)  # Small delay to ensure tabs open correctly

    print("All tabs opened, waiting for 5 minutes...")
    time.sleep(300)  # Wait for 5 minutes

    tab_handles = get_cmd_pids()
    close_tabs(tab_handles)
    print("All tabs closed, reopening tabs one by one every 5 minutes...")

    for i in range(10):
        open_new_tab(i + 1)
        time.sleep(300)  # Wait for 5 minutes before opening the next tab
