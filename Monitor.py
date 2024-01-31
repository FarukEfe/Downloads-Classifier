import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileCreatedEvent

# We need to specify what the eventhandler does when file event returns
class CustomHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        pass
    
class Monitor:

    event_handler = FileSystemEventHandler()

    def __init__(self, directory):
        self.directory = directory
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while self.observer.is_alive():
                self.observer.join(1)
                time.sleep(0.5)
        finally:
            self.observer.stop()
            self.observer.join()