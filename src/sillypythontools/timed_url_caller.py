# encoding: utf-8

# === description ====
# This script is designed to open a specified URL in the default web browser at a predetermined point in time.
# It uses the `webbrowser` module to open the URL and the `datetime` module to handle time comparisons.

# === usage ====
# 1. Set the `url` variable to the desired URL you want to open.
# 2. Set the `time_to_call` variable to the desired time in the format "YYYY-MM-DD HH:MM:SS".
# 3. Run the script. It will wait until the specified time and then open the URL in the default web browser.

# ==== dependencies ====
import time
import webbrowser
from datetime import datetime
from rich.progress import Progress
from progress.spinner import PieSpinner

# ==== parameters ====
url: str = "..."  # the url to call

## = time controls =
time_to_call: str = "2026-11-08 23:59:59"  # format: YYYY-MM-DD HH:MM:SS

# thresholds for switching between different checking intervals
idle_threshold: int = (
    60  # seconds to timepoint when we switch to more frequent checking
)
approaching_threshold: int = (
    10  # seconds to timepoint when we switch to continuous checking
)

# wait intervals for checking the time
wait_interval_idle: int = 10  # seconds to wait before checking the time again
wait_interval_approaching: int = 1  # seconds to wait before checking the time again

# ==== preparation ====
# convert the time string to a datetime object
time_to_call_dt = datetime.strptime(time_to_call, "%Y-%m-%d %H:%M:%S")


# progress elements - ready, set, go spinner
def ReadySetGoSpinner():
    spinner = PieSpinner(message="Primed... ", fill="█", empty_fill="░")
    return spinner


# ==== main logic ====
# logic to open browser and call the url at the specified time
def open_browser_and_call_url():
    webbrowser.get().open(url)


def wait_until_time_to_call():
    with Progress() as pbar:
        # prepare the progress bar
        initial_timedelta = (time_to_call_dt - datetime.now()).total_seconds()
        task = pbar.add_task(
            "Approaching time to call the url",
            total=initial_timedelta - approaching_threshold,
        )

        while datetime.now() < time_to_call_dt:
            timedelta = (time_to_call_dt - datetime.now()).total_seconds()
            if timedelta < approaching_threshold:
                pbar.update(task, advance=initial_timedelta - timedelta)
                break  # exit the loop to start the ready set go spinner
            elif timedelta < idle_threshold:
                pbar.update(task, advance=initial_timedelta - timedelta)
                initial_timedelta = (
                    timedelta  # update the initial timedelta for the next iteration
                )
                time.sleep(wait_interval_approaching)
            else:
                pbar.update(task, advance=initial_timedelta - timedelta)
                initial_timedelta = (
                    timedelta  # update the initial timedelta for the next iteration
                )
                time.sleep(wait_interval_idle)


def ready_set_go():
    print(f"Preparing to call the url: {url}. Current time: {datetime.now()}.")
    with ReadySetGoSpinner() as spinner:
        while datetime.now() < time_to_call_dt:
            spinner.next()
        open_browser_and_call_url()


def cleanup():
    print(f"Finished calling the url: {url}. Current time: {datetime.now()}.")
    print("Cleaning up...")
    # add any cleanup logic here if needed


def main():
    if not webbrowser.get():
        print("No active browser found. Please check your configuration.")
        return False
    if datetime.now() >= time_to_call_dt:
        print(
            f"The specified time to call the url: {time_to_call} has already passed. Current time: {datetime.now()}."
        )
        return False
    else:
        wait_until_time_to_call()
        ready_set_go()
        cleanup()
        return True


# ==== run ====
if __name__ == "__main__":
    main()
