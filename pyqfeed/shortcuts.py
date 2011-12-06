import datetime, Queue, types
import History, Listener

class _QueueProducer(Listener.Listener):
    def __init__(self, q):
        self.__q = q
        
    def on_message(self, message, **kwargs):
        self.__q.put(message)
    
    def on_data_end(self):
        self.__q.put(None)
        
    def on_error(self, message, **kwargs):
        self.__q.put(None)
         
def history(instrument, start_date, num_days=100000, host="localhost", port=9100):
    '''
    Generates history lines for a given instrument
    '''
    if type(start_date) == types.StringType:
        start_date = datetime.date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))

    _q = Queue.Queue()
    _qp = _QueueProducer(_q)
    
    client = History.HistoryClient((host, port))
    client.set_listener('', _qp)
    client.getHistory(instrument, start_date, num_days)
    
    while 1:
        try:
            # Wait until a new message is available
            message = _q.get()
            if message is None: 
                break
            yield message
        except KeyboardInterrupt:
            break
        
    client.del_listener('')
    
if __name__ == "__main__":
    for line in history("QQQ", datetime.date.today()):
        print line