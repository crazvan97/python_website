import os
import time
import shutil
import hashlib
import argparse
import threading
from datetime import timedelta, datetime


class ParseArguments:
    def __init__(self):
        self.arguments = self.parse_arguments()

    @staticmethod
    def check_interval(value, max_value):
        int_value = int(value)
        if int_value < 1 or int_value > max_value:
            raise argparse.ArgumentTypeError(f"Value must be in interval: [1, {max_value}]. You entered {value}.")
        return int_value

    @staticmethod
    def check_hour_format(value):
        try:
            return datetime.strptime(value, "%H:%M")
        except ValueError:
            raise argparse.ArgumentTypeError(f"The time must be in 24-hour format 'HH:MM' (e.g. 19:45)")

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="""
            The script synchronizes the contents of folder2 based on folder1, at a specified future time or at regular intervals.
            Once the script was started, the synchronization could also be manually triggered, on-demand, before scheduled time or 
            between periodic intervals, at any time, by typing 'sync' in terminal.""",
            usage="""
            python %(prog)s <folder1> <folder2> [-s SECONDS] [-m MINUTES] [-hr HOURS] [-d DAYS] [-t TIME] [-h].""",
            epilog="""Examples:
            - For Scheduled sync at 19:45, run: python %(prog)s /path/to/folder1 /path/to/folder2 -t 19:45
            - For Periodic sync at every 3 hours 4 minutes and 5 seconds, run: python %(prog)s /path/to/folder1 /path/to/folder2 -hr 3 -m 4 -s 5""",
            formatter_class=argparse.RawTextHelpFormatter)

        parser.add_argument("folder1", type=str, help="First folder path")
        parser.add_argument("folder2", type=str, help="Second folder path")
        parser.add_argument("-s", "--seconds", type=lambda value: self.check_interval(value, max_value=60),
                            help="For periodic sync, specify the seconds interval value.")
        parser.add_argument("-m", "--minutes", type=lambda value: self.check_interval(value, max_value=60),
                            help="For periodic sync, specify the minutes interval value.")
        parser.add_argument("-hr", "--hours", type=lambda value: self.check_interval(value, max_value=24),
                            help="For periodic sync, specify the hours interval value.")
        parser.add_argument("-d", "--days", type=lambda value: self.check_interval(value, max_value=30),
                            help="For periodic sync, specify the days interval value.")
        parser.add_argument("-t", "--time", type=self.check_hour_format,
                            help="For scheduled sync, specify the time in 24-hour format (e.g. 19:45).")

        return parser.parse_args()

    def get_interval_schedule(self):
        if any([self.arguments.seconds, self.arguments.minutes, self.arguments.hours, self.arguments.days]):
            if self.arguments.time:
                print(f"[ERROR] -t could not be used together with interval params (e.g. -s, -m, -hr or -d)")
                exit(0)
            else:
                # Handle periodic sync
                interval = timedelta()
                if self.arguments.seconds:
                    interval += timedelta(seconds=self.arguments.seconds)
                if self.arguments.minutes:
                    interval += timedelta(minutes=self.arguments.minutes)
                if self.arguments.hours:
                    interval += timedelta(hours=self.arguments.hours)
                if self.arguments.days:
                    interval += timedelta(days=self.arguments.days)
                return interval, None

        elif self.arguments.time:
            return None, self.arguments.time
        else:
            print(f"[ERROR] Invalid arguments. Run: python {os.path.basename(__file__)} --help.")
            exit(0)


class FolderSync:
    def __init__(self, folder1: str, folder2: str, interval: timedelta, schedule: datetime):
        self.folder1 = folder1
        self.folder2 = folder2
        self.interval = interval
        self.schedule = schedule
        self.last_sync_time = None
        # Lock to ensure that manual and periodic syncs don't run at the same time
        self.sync_lock = threading.Lock()

    @staticmethod
    def generate_file_hash(file_path):
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as file:
            while chunk := file.read(1048576):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    def _folder_sync(self):
        for dirpath, dirnames, filenames in os.walk(self.folder1):
            relpath = os.path.relpath(dirpath, self.folder1)
            folder2_dirpath = os.path.join(self.folder2, relpath)

            if not os.path.exists(folder2_dirpath):
                os.makedirs(folder2_dirpath)

            for file in filenames:
                folder1_file_path = os.path.join(dirpath, file)
                folder2_file_path = os.path.join(folder2_dirpath, file)
                if (not os.path.exists(folder2_file_path)
                        or self.generate_file_hash(folder1_file_path) != self.generate_file_hash(folder2_file_path)):
                    shutil.copy2(src=folder1_file_path, dst=folder2_file_path)

    def _interval_sync(self):
        while True:
            if self.last_sync_time is None or datetime.now() - self.last_sync_time >= self.interval:
                # lock before starting sync
                with self.sync_lock:
                    print(f"[{datetime.now()}] Periodic synchronization starting.")
                    # self._folder_sync()
                    self.last_sync_time = datetime.now()
                    print(f"[{datetime.now()}] Periodic synchronization completed.")
            time.sleep(1)

    def _scheduled_sync(self):
        current_time = datetime.strptime(datetime.now().strftime('%H:%M'), "%H:%M")
        if current_time > self.schedule:
            print(f"The time {self.schedule} has already passed today. It will be scheduled for tomorrow.")
            self.schedule = (datetime.strptime(self.schedule.strftime('%H:%M'), '%H:%M') + timedelta(days=1)).strftime('%H:%M')
        while True:
            if current_time >= self.schedule:
                # lock before starting sync
                with self.sync_lock:
                    print(f"[{datetime.now()}] Scheduled synchronization starting.")
                    # self._folder_sync()
                    self.last_sync_time = datetime.now()
                    print(f"[{datetime.now()}] Scheduled synchronization completed.")
                break
            time.sleep(60)

    def start_auto_sync(self):
        target = self._interval_sync if self.interval else self._scheduled_sync
        sync_thread = threading.Thread(target=target)
        sync_thread.daemon = True  # Allow the thread to exit when the main program exits
        sync_thread.start()

    def manual_sync(self):
        with self.sync_lock:
            print(f"[{datetime.now()}] Manual synchronization starting.")
            # self._folder_sync()
            # print(f"[{datetime.now()}] Periodic synchronization completed.")

def main():
    parser = ParseArguments()
    interval, schedule = parser.get_interval_schedule()
    print(interval, schedule)

    folder_sync = FolderSync(parser.arguments.folder1, parser.arguments.folder2, interval=interval, schedule=schedule)
    folder_sync.start_auto_sync()

    try:
        while True:
            text = input("Type 'sync' to trigger now a manual synchronization\n")
            if "sync" == text.strip():
                folder_sync.manual_sync()
    except KeyboardInterrupt:
        print("Program interrupted.")
        exit(0)


if __name__ == "__main__":
    main()

"""
INTREBARI:
ce fac daca gasesc fisiere/foldere in folder2 care nu apar si in folder1?
cat de des apar modificari in folder1?
large directories inseamna fisiere de mari dimensiuni sau doar fisiere numeroase?
"""
