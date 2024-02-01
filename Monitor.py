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
        # Should store different directories to store different file types (pdfs into docments, jpeg into images, etc))

    def on_modified(self, event):
        # Should move the contents of downloads into their respective directory
        print("Changes made.")
        print(f"Event Info: {event}\n")
        if event.is_directory:
            # Gather directory contents
            pass
        else:
            file_format = event.src_path.split(".")[-1]

        

    def on_any_event(self, event):
        print(event.event_type)
        print(event.src_path)

class Monitor:

    def __init__(self, directory):
        self.directory = directory
        self.observer = Observer()
        self.event_handler = CustomHandler()
        self.dest_handler = DestinationHandler()
        

    def start(self):
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join(1)
                time.sleep(0.05)
        finally:
            self.observer.stop()
            self.observer.join()


if __name__ == "__main__":
    process = Subprocess()
    directory = process.ask_user_folder()
    monitor = Monitor(directory)
    monitor.start()