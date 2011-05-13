import datetime, threading, logging
import Client

class HistoryClient(object):
	def __init__(self, (host, port) = ("127.0.0.1", 9100)):
		self.host = host
		self.port = port
		self.instrument = None
		self.exit_thread = threading.Event()

	def getHistory(self, instrument, date, num_days=1):
		self.instrument = instrument

		self.client = Client.Client((self.host, self.port))
		self.client.set_listener('', self)
		self.client.start()
		self.client.send("HTD,%s,%i,,,,1" % (self.instrument, num_days))

		import time
		time.sleep(1)

		self.exit_thread.wait()

	def stop(self):
		self.disconnect()

	def disconnect(self):
		logging.debug("Trying to disconnect...")
		self.client.stop()
		self.exit_thread.set()

	def on_message(self, data):
		if data.startswith("E,!"):
			self.disconnect()
		elif data.startswith("!ENDMSG!"):
			self.disconnect()
		else:
			print data
			pass

		split_data = data.split(",")
		
	
