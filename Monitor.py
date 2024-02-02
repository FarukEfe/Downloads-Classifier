import time, os, sys, functools
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Subprocess import Subprocess
from DestinationHandler import DestinationHandler

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
            pass
        else:
            self.handler(event.src_path)

        

    def on_any_event(self, event):
        print(event.event_type)
        print(event.src_path)

class Monitor:

    queue: {str:str} = {}

    def __init__(self, directory):
        self.directory = directory
        self.observer = Observer()
        self.event_handler: FileSystemEventHandler = None
        self.dest_handler = DestinationHandler()

    # Adds new job to queue 
    def add_to_queue(self, file_path):
        file_format = file_path.split(".")[-1] # Get file format
        destination = self.dest_handler.get_destination(file_format) # Get destination by format
        # Ignores job if there's no assigned destination
        if destination is None or self.queue[file_path] != None:
            return
        # Add new job to dictionary
        self.queue[file_path] = destination
        
    # Event handler and observer setup
    def start(self):
        self.event_handler = CustomHandler(self.add_to_queue)
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
    
    # Return if watchdog observer is running
    def is_alive(self):
        return self.observer.is_alive()
    
    def join(self, timeout: float | None):
        monitor.observer.join(timeout)
    
    def stop(self):
        monitor.observer.stop()


if __name__ == "__main__":
    process = Subprocess()
    directory = process.ask_user_folder()
    monitor = Monitor(directory)
    monitor.start()
    try:
        while monitor.is_alive():
            for key in monitor.queue.keys(): # Iterate through all keys
                dest = monitor.queue[key] # Get destination
                Subprocess.move_file(file_dir=key,destination=dest) # Perform job
                del monitor.queue[key] # Remove from queue
            # Monitor cycle
            monitor.join(1)
            time.sleep(0.05)
    finally:
        monitor.stop()
        monitor.join()