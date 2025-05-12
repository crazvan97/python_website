"""
The script synchronizes the contents of folder2 based on folder1, at a specified future time or at regular intervals.
Once the script was started, the synchronization could also be manually triggered, on-demand, before scheduled time or
between periodic intervals, at any time, by typing 'sync' in terminal. Type 'quit' in terminal to stop the script.

usage = python sync_folders.py <folder1> <folder2> [-s SECONDS] [-m MINUTES] [-hr HOURS] [-d DAYS] [-t TIME] [-h].
help = python sync_folders.py --help

Examples:
    -For Scheduled sync at 19:45, run:
        python sync_folders.py /path/to/folder1 /path/to/folder2 -t 19:45
    -For Periodic sync at every 3 hours 4 minutes and 5 seconds, run:
        python sync_folders.py /path/to/folder1 /path/to/folder2 -hr 3 -m 4 -s 5
"""

import os
import time
import shutil
import hashlib
import logging
import argparse
import threading
from datetime import timedelta, datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_logger(filename) -> logging.Logger:
    """
    Used to create a custom logger object.
    :param filename: name of the file where logs are saved
    :return: logging.Logger object
    """
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.WARNING, "W")

    logging.basicConfig(
        filename=filename,
        encoding="utf-8",
        filemode="a",
        datefmt="%y-%m-%d %H:%M:%S",
        format="[{asctime}][{levelname}] {message} - {funcName}",
        style="{",
        level=logging.INFO,
    )
    return logging.getLogger()


logger = get_logger("folder_sync_logs.log")


class ParseArguments:
    def __init__(self):
        self.arguments = self.parse_arguments()

    @staticmethod
    def check_interval(value, max_value) -> int:
        """
        Checks if value is in interval [1, max_value]
        :param value: input value
        :param max_value: maximum value accepted
        :return: value as an integer
        """
        int_value = int(value)
        if int_value < 1 or int_value > max_value:
            raise argparse.ArgumentTypeError(f"Value must be in interval: [1, {max_value}]. You entered {value}.")
        return int_value

    @staticmethod
    def check_hour_format(value) -> datetime:
        """
        Create datetime object from string value. Raise ArgumentTypeError if string does not have 24-hour format.
        :param value: input string representing scheduled time
        :return: datetime object
        """
        try:
            return datetime.combine(date.today(), datetime.strptime(value, "%H:%M").time())
        except ValueError:
            raise argparse.ArgumentTypeError("The time must be in 24-hour format 'HH:MM' (e.g. 19:45)")

    def parse_arguments(self) -> argparse.Namespace:
        """
        Used to create a small overview for new script users.
        Parse input arguments when the script is started. Every argument is checked based on particular constraints.
        Not accepted arguments will stop the script.
        :return: arguments object
        """
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

    def get_interval_schedule(self) -> tuple:
        """
        Used to decide which sync method (interval or schedule) to be used based on arguments.
        Interval arguments (-s, -m, -hr, -d) could not be used together with schedule argument (-t).
        :return: (interval, schedule)
        """
        if any([self.arguments.seconds, self.arguments.minutes, self.arguments.hours, self.arguments.days]):
            if self.arguments.time:
                print("[ERROR] -t could not be used together with interval params (e.g. -s, -m, -hr or -d)")
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
        # Lock to ensure that manual and auto syncs don't run at the same time
        self.sync_lock = threading.Lock()

    @staticmethod
    def file_hash(file_path) -> str:
        """
        Generates hash value of file_path. Files will be read in chuncks of 1MB.
        :param file_path:
        :return: hash value of file_path
        """
        md5_hash = hashlib.md5()
        with open(file_path, 'rb') as file:
            while chunk := file.read(1048576):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    @staticmethod
    def process_file(folder1: str, folder2: str, dirpath: str, filenames: list) -> None:
        """
        Used to compare dirpath content from folder1 and folder2. If a file from folder2 does not exist or has a
        different hash value that the one from folder1, will be replaced from folder1.
        :param folder1: Folder1 full path
        :param folder2: Folder2 full path
        :param dirpath: folder from folder1
        :param filenames: files from folder1
        :return: None
        """
        relpath = os.path.relpath(dirpath, folder1)
        folder2_dirpath = os.path.join(folder2, relpath)
        if not os.path.exists(folder2_dirpath):
            logger.warning(f'Creating folder [{relpath}] in [{folder2}]')
            os.makedirs(folder2_dirpath)

        for file in filenames:
            file1_path = os.path.join(dirpath, file)
            file2_path = os.path.join(folder2_dirpath, file)
            if not os.path.exists(file2_path) or FolderSync.file_hash(file1_path) != FolderSync.file_hash(file2_path):
                logger.warning(f"Sync file [{file}] from [{folder2_dirpath}].")
                shutil.copy2(src=file1_path, dst=file2_path)

    @staticmethod
    def remove_files(folder2: str, folder1: str, dirpath: str, filenames: list) -> None:
        relpath = os.path.relpath(dirpath, folder2)
        folder1_dirpath = os.path.join(folder1, relpath)

        if not os.path.exists(folder1_dirpath):
            logger.warning(f'Removing folder [{dirpath}] in [{folder2}]')
            shutil.rmtree(dirpath)

        else:
            for file in filenames:
                file2_path = os.path.join(dirpath, file)
                file1_path = os.path.join(folder1_dirpath, file)
                if not os.path.exists(file1_path):
                    logger.warning(f"Remove file [{file}] from [{folder2}].")
                    os.remove(file2_path)

    def _folder_sync(self) -> None:
        """
        Used to create a pool of executors.
        :return: None
        """
        with ThreadPoolExecutor() as executor:
            results = [executor.submit(self.process_file, self.folder1, self.folder2, dirpath, filenames)
                                              for dirpath, _, filenames in os.walk(self.folder1)]

            results.extend([executor.submit(self.remove_files, self.folder2, self.folder1, dirpath, filenames)
                       for dirpath, _, filenames in os.walk(self.folder2)])

            for result in as_completed(results):
                try:
                    result.result()
                except Exception as exception:
                    logger.exception(exception)
                    exit(0)
        print(f"Last sync: {datetime.now()}. Type 'sync' to trigger sync now or 'quit' to stop the script.")

    def _interval_sync(self) -> None:
        """
        Used to trigger periodic syncs (accordingly with interval parameter) in an infinite loop.
        :return: None
        """
        while True:
            # lock before starting sync
            with self.sync_lock:
                logger.info("Sync started.")
                self._folder_sync()
                logger.info(f"Sync completed. Next sync after {self.interval.seconds} seconds")
            time.sleep(self.interval.seconds)

    def _scheduled_sync(self) -> None:
        """
        Used to perform folder sync at the scheduled time.
        After sync is done, notify main function to stop the script execution.
        :return: None
        """
        if datetime.now() > self.schedule:
            self.schedule = self.schedule + timedelta(days=1)
            logger.info(f"Your time has passed today. Scheduled for tomorrow at {self.schedule.strftime('%H:%M')}")

        print(f'Sync scheduled for: {self.schedule}')
        waiting_time = (self.schedule - datetime.now()).seconds
        logger.info(f'Waiting {waiting_time} seconds before starting scheduled sync')
        time.sleep(waiting_time)
        with self.sync_lock:
            logger.info("Sync started.")
            self._folder_sync()
            logger.info("Sync completed.")

    def start_auto_sync(self) -> threading.Thread:
        """
        Used to trigger the sync method in a new thread, acordingly with input parameters (schedule or interval).
        :return: thread object created
        """
        logger.info(f'- Start sync folder [{self.folder2}] from [{self.folder1}].')
        sync_thread = threading.Thread(target=self._interval_sync if self.interval else self._scheduled_sync)
        sync_thread.daemon = True
        sync_thread.start()
        return sync_thread

    def manual_sync(self) -> None:
        """
        Used to trigger on-demand sync, at any time.
        :return: None
        """
        with self.sync_lock:
            logger.info("Sync started")
            self._folder_sync()
            logger.info("Sync completed")


def get_input_thread(read_input: list) -> None:
    """
    Read user input from console and append it to a list
    :param read_input: contains inputs read from console
    :return: None
    """
    while True:
        user_input = input().strip().lower()
        read_input.append(user_input)
        if "quit" == user_input:
            break


def main():
    parser = ParseArguments()
    interval, schedule = parser.get_interval_schedule()

    folder_sync = FolderSync(parser.arguments.folder1, parser.arguments.folder2, interval, schedule)
    auto_sync = folder_sync.start_auto_sync()

    # Start a dedicated thread to read user input from console
    input_list = []
    input_thread = threading.Thread(target=get_input_thread, args=(input_list,))
    input_thread.daemon = True
    input_thread.start()

    print("Type 'sync' to trigger sync now or 'quit' to stop the script.")
    while auto_sync.is_alive():
        if input_list:
            text = input_list.pop(0)
            print(text)
            if "sync" == text:
                folder_sync.manual_sync()
            if "quit" == text:
                logger.info("'quit' was received, stop the script")
                break
        time.sleep(1)


if __name__ == "__main__":
    main()
