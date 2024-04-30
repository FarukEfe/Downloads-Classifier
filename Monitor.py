import time, os, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Workers.Subprocess import Subprocess
from Workers.DestinationHandler import DestinationHandler

# We need to specify what the eventhandler does when file event returns
class CustomHandler(FileSystemEventHandler):

    def __init__(self, handler: callable):
        super().__init__()
        self.handler = handler

    def on_modified(self, event):
        # Should move the contents of downloads into their respective directory
        print("Changes made.")
        print(f"Event Info: {event}\n")
        if event.is_directory:
            # Gather directory contents
            file_paths = []
            w = os.walk(event.src_path)
            for root, _, files in w:
                for file in files:
                    p = os.path.join(root, file)
                    file_paths.append(p)
            # Add all files to queue
            for path in file_paths:
                self.handler(path)
        else:
            self.handler(event.src_path)

class Monitor:

    queue: dict[str:str] = {}
    finished: dict[str:str] = {}

    def __init__(self):
        self.directory = None
        self.observer = Observer()
        self.event_handler: FileSystemEventHandler = None
        self.dest_handler = DestinationHandler()

    def list_finished_jobs(self) -> list[str]:
        texts = []
        for key in list(self.finished.keys()):
            texts.append(f"{key} moved to {self.finished[key]}")
        return texts

    def set_directory(self,directory):
        self.directory = directory

    # Adds new job to queue 
    def add_to_queue(self, file_path):
        file_format = file_path.split(".")[-1] # Get file format
        destination = self.dest_handler.get_destination(file_format) # Get destination by format
        # Ignores job if there's no assigned destination
        if destination is None:
            return
        # Add new job to dictionary
        self.queue[file_path] = destination
        
    # Event handler and observer setup
    def start(self) -> int:
        if self.directory == None:
            return 0
        self.event_handler = CustomHandler(self.add_to_queue)
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        return 1
    
    # Return if watchdog observer is running
    def is_alive(self):
        return self.observer.is_alive()

    # Check if the monitor can start
    def can_start(self):
        return self.directory != None and os.path.exists(self.directory) and os.path.isdir(self.directory)
    
    def join(self, timeout: float):
        self.observer.join(timeout)
    
    def stop(self):
        self.observer.stop()
    
    def delete_keys(self, keys: list[str]):
        for key in keys:
            self.finished[key] = self.queue[key]
            del self.queue[key]
    
    def flush_logs(self):
        self.finished = {}
    
    def flush_jobs(self):
        self.queue = {}

if __name__ == "__main__":
    process = Subprocess()
    directory = process.ask_user_folder()
    test_file = process.ask_user_folder() # T
    monitor = Monitor(directory)
    monitor.dest_handler.set_destination("pdf",test_file) # T
    monitor.start()
    try:
        while monitor.is_alive():
            remove_keys = []
            for key in monitor.queue.keys(): # Iterate through all keys
                dest = monitor.queue[key] # Get destination
                process.move_file(key,dest) # Perform job
                remove_keys.append(key) # Append to deleting keys
            
            monitor.delete_keys(remove_keys) # Delete keys after all jobs are done
            
            # Monitor cycle
            monitor.join(1)
            time.sleep(1)
    finally:
        monitor.stop()
        monitor.join(0)