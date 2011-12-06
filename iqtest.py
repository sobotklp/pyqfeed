#!/usr/bin/env python
'''
Simple front end for IQFeed client.
Simply issues a command and writes out whatever it gets back
'''
import os, sys, logging, optparse, time

import pyqfeed.OldClient
import pyqfeed.Listener

class IQTestListener(pyqfeed.Listener.Listener):
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.fd = open(self.outfile, "wb")
        else:
            self.fd = sys.stdout

    def on_error(self, message):
        pass
    
    def on_message(self, message):
        self.fd.write(message + "\n")

def iqtest(host, port, command, output_filename=None):
    listener = IQTestListener(output_filename)
    
    client = pyqfeed.OldClient.Client((host, port))
    client.start()
    client.set_listener('', listener)
    client.send(command)

    # Wait for disconnect or Ctrl-C
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()
    
def main():
     # Vanilla command-line arg parsing. Run with -h to see pretty output"
    parser = optparse.OptionParser()
    parser.add_option('-p', dest="port", type="int", default=5009, help="IQFeed service port. Default=5009")
    parser.add_option('-s', dest="host", type="string", default="127.0.0.1", help="IQFeed service host. Default=localhost")
    parser.add_option('-c', dest="command", type="string", help="Commands to send to IQfeed")
    parser.add_option('-o', dest="outfile", type="string", default=None, help="Save IQfeed output to this file")
    parser.add_option("--debug", action="store_true", dest="debug", default=False, help="Debug this script?")    
    (options, args) = parser.parse_args()
    
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
        
    if not options.command:
        parser.error("Please specify a command with -c")
        
    iqtest(options.host, options.port, options.command, options.outfile)
    
if __name__ == "__main__":
    main()