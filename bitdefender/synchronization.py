import os
import shutil
import time
import hashlib
import threading
from datetime import datetime, timedelta


class FolderSync:
    def __init__(self, folder1: str, folder2: str, sync_interval=None, interval_unit='seconds'):
        self.folder1 = folder1
        self.folder2 = folder2
        self.sync_interval = sync_interval
        self.interval_unit = interval_unit
        self.last_sync_time = None
        self.stop_event = threading.Event()

        # Lock to ensure that manual and periodic syncs don't run at the same time
        self.sync_lock = threading.Lock()

        # Valid interval units
        self.valid_units = ['seconds', 'minutes', 'hours', 'days']

        # Validate synchronization interval
        if self.sync_interval is not None:
            if self.interval_unit not in self.valid_units:
                raise ValueError(f"Invalid unit. Choose from {self.valid_units}")
            if self.sync_interval <= 0:
                raise ValueError("Interval must be a positive integer.")

    @staticmethod
    def _generate_file_hash(file_path):
        """Generate the hash of a file to check content equality."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Read file in chunks
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _sync_folders(self):
        """Synchronize files from Folder 1 to Folder 2."""
        for root, dirs, files in os.walk(self.folder1):
            relative_path = os.path.relpath(root, self.folder1)
            folder2_path = os.path.join(self.folder2, relative_path)

            # Create subfolders in Folder 2 if not exist
            if not os.path.exists(folder2_path):
                os.makedirs(folder2_path)

            for file in files:
                file1_path = os.path.join(root, file)
                file2_path = os.path.join(folder2_path, file)

                # If file doesn't exist in Folder 2 or differs in content, copy it
                if not os.path.exists(file2_path) or self._generate_file_hash(file1_path) != self._generate_file_hash(
                        file2_path):
                    shutil.copy2(file1_path, file2_path)
                    print(f"[{datetime.now()}] File {file} synchronized from {file1_path} to {file2_path}")

    def _schedule_sync(self):
        """Periodically synchronize the folders."""
        while not self.stop_event.is_set():
            if self.last_sync_time is None or datetime.now() - self.last_sync_time >= self._get_sync_interval():
                # Acquire the lock before starting synchronization
                with self.sync_lock:
                    print(f"[{datetime.now()}] Periodic synchronization starting.")
                    self._sync_folders()
                    self.last_sync_time = datetime.now()
                    print(f"[{datetime.now()}] Periodic synchronization completed.")
            time.sleep(1)

    def _get_sync_interval(self):
        """Get the interval as a timedelta object."""
        if self.interval_unit == 'seconds':
            return timedelta(seconds=self.sync_interval)
        elif self.interval_unit == 'minutes':
            return timedelta(minutes=self.sync_interval)
        elif self.interval_unit == 'hours':
            return timedelta(hours=self.sync_interval)
        elif self.interval_unit == 'days':
            return timedelta(days=self.sync_interval)

    def start_periodic_sync(self):
        """Start periodic synchronization in a background thread."""
        if self.sync_interval is None:
            raise ValueError("Synchronization interval must be specified.")
        sync_thread = threading.Thread(target=self._schedule_sync)
        sync_thread.daemon = True  # Allow the thread to exit when the main program exits
        sync_thread.start()

    def manual_sync(self):
        """Manually synchronize the folders."""
        # Acquire the lock before starting manual synchronization
        with self.sync_lock:
            print(f"[{datetime.now()}] Manual synchronization starting.")
            self._sync_folders()
            print(f"[{datetime.now()}] Manual synchronization completed.")

    def stop_periodic_sync(self):
        """Stop the periodic synchronization."""
        self.stop_event.set()


# Example usage
if __name__ == "__main__":
    path1 = r"C:\Users\razva\Desktop\New folder"
    path2 = r"C:\Users\razva\Desktop\New folder (2)"

    # Initialize FolderSync with periodic sync every 1 minute
    sync = FolderSync(path1, path2, sync_interval=1, interval_unit='minutes')

    # Start periodic synchronization in the background
    sync.start_periodic_sync()

    # Allow manual synchronization at any time
    # For instance, synchronize immediately if required
    sync.manual_sync()

    # To stop periodic sync after some time, call:
    # sync.stop_periodic_sync()

    # Keep the program running (simulate your app is running)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Program interrupted.")
        sync.stop_periodic_sync()

"""
- not implemented: one-time synchronization at a specified future time.
- create decorator for logging
- try to add multiprocessing to sync method. -> IMPORTANT
"""