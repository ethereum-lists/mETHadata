import sys
import time
import logging

# https://github.com/gorakhargosh/watchdog#example-api-usage
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from subprocess import call

class PyHandler(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path.lower().endswith('.py'):
            print("(compile.py) recompiling...")
            call(["python", "compile.py"])


class EvHandler(LoggingEventHandler):
    def dispatch(self, event):
        print("recompiling...")
        call(["python", "compile.py"])

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

path = "./templates"

event_handler = EvHandler()

observer = Observer()
observer.schedule(event_handler, "./templates", recursive=True)
observer.schedule(PyHandler(), '.', recursive=False)
#observer.schedule(event_handler, '../tokens', recursive=True)
observer.schedule(event_handler, '../entities', recursive=True)


observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()