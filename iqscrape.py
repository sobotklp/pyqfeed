#!/usr/bin/env python
'''
Scrape data from a basket of stocks from IQfeed
'''

import os, sys, logging, optparse, time

import pyqfeed.Client

class IQTestListener(object):
    def __init__(self, outfile=None):
        self.outfile = outfile
        if self.outfile:
            self.fd = open(self.outfile, "wb")
        else:
            self.fd = sys.stdout

    def on_error(self, message):
        pass
    
    def on_message(self, message):
        if message.startswith('F'):
            self.fd.write(message + "\n")


def loadSymbolsFromFile(filename):
    base, ext = os.path.splitext(filename)
    symbols = []
    
    if ext.lower() == ".csv":
        for row in csv.reader(open(filename, "rb")):
            symbols.append( row[0] )
    
    return symbols

def scrapeData(host, port, symbols, output_filename=None):
    listener = IQTestListener(output_filename)
    
    # Set up the IQfeed client.
    client = pyqfeed.Client.Client((host, port))
    client.start()
    client.set_listener('', listener)
    
    # Watch all the symbols we're interested in.
    for symbol in symbols:
        client.send("w%s" % symbol)

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
    parser.add_option('-i', dest="input_file", type="string", help="Input file")
    parser.add_option('-o', dest="output_file", type="string", default=None, help="Save IQfeed output to this file")
    parser.add_option("--debug", action="store_true", dest="debug", default=False, help="Debug this script?")    
    (options, args) = parser.parse_args()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
        
    if not options.input_file:
        parser.error("Please specify an input file with -i")

    symbols = loadSymbolsFromFile(options.input_file)
    scrapeData(options.host, options.port, symbols, options.output_file)
    
if __name__ == "__main__":
    main()