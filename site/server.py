import sys
import time
import logging

import json

# https://github.com/gorakhargosh/watchdog#example-api-usage
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from subprocess import call

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        with open("entities{}.html".format(self.path)) as f:
            self.wfile.write(f.read().encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself


        data = json.loads(post_data.decode('utf-8'))
        logging.info(json.dumps(data, indent=2))

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))




        file_name = '../entities/{}'.format(data['fname'])
        with open(file_name, 'w') as out_file:
            out_file.write(json.dumps(data['e'], indent=2))



def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

exit()

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
observer.schedule(event_handler, '../tokens', recursive=True)

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()