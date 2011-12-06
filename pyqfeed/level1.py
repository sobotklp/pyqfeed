import re, datetime

from client import IQConnectSocketClient
from dispatcher import Dispatcher

from exception import PyQFeedException

class Level1MessageHandler:
    def on_message(self, *args, **kwargs):
        # Catch-all message handler
        pass
    
    def on_system_connected(self, *args, **kwargs):
        print "Connected!"
        
    def on_system_disconnected(self, *args, **kwargs):
        print "Disconnected!"

    def on_time_message(self, dt, **kwargs):
        print "The time is", dt
        
    def on_fundamental_message(self, **kwargs):
        print kwargs['data']
    
    def on_update_message(self, **kwargs):
        print kwargs['data']
        
    def on_summary_message(self, **kwargs):
        print kwargs['data']
        
    def on_stats_message(self, **kwargs):
        print kwargs['data']
        
    def on_fundamental_fieldnames_message(self, **kwargs):
        print kwargs['data']

    def on_update_fieldnames_message(self, **kwargs):
        print kwargs['data']
        
class Level1Mixin:
    def _handle_system_message(self, msg):
        msg_type = msg[2:].partition(',')[0]
        if msg_type == 'KEY':
            # Old authentication method. Ignore
            pass
        elif msg_type == 'SERVER CONNECTED':
            self._dispatch_message('on_system_connected', data=msg)
        elif msg_type == 'SERVER DISCONNECTED':
            self._dispatch_message('on_system_disconnected', data=msg)
        elif msg_type == 'STATS':
            self._dispatch_message('on_stats_message', data=msg)
        elif msg_type == 'FUNDAMENTAL FIELDNAMES':
            self._dispatch_message('on_fundamental_fieldnames_message', data=msg)
        elif msg_type == 'UPDATE FIELDNAMES':
            self._dispatch_message('on_update_fieldnames_message', data=msg)            
        else:
            pass
            
    def _handle_time_message(self, msg):
        dt = datetime.datetime.strptime(msg[2:].strip(), '%Y%m%d %H:%M:%S')
        self._dispatch_message('on_time_message', dt,  data=msg)

    def _handle_fundamental_message(self, msg):
        self._dispatch_message('on_fundamental_message', data=msg)
        pass
    
    def _handle_summary_message(self, msg):
        self._dispatch_message('on_summary_message', data=msg)
        pass

    def _handle_update_message(self, msg):
        self._dispatch_message('on_update_message', data=msg)
        pass

    def new_message(self, data):
        if data[0] == 'S':
            self._handle_system_message(data)
        elif data[0] == 'T':
            self._handle_time_message(data)
        elif data[0] == 'F':
            self._handle_fundamental_message(data)
        elif data[0] == 'P':
            self._handle_summary_message(data)
        elif data[0] == 'Q':
            self._handle_update_message(data)

        self._dispatch_message('on_message', data)
    
class Level1Client(IQConnectSocketClient, Level1Mixin):
    new_message = Level1Mixin.new_message
    
    def watch(self, symbol):
        '''
        Begin watching a symbol
        '''
        self.send('w%s' % symbol)
                
    def unwatch(self, symbol):
        '''
        Stop watching a symbol
        '''
        self.send('r%s' % symbol)
    
    def enable_regional_quotes(self, symbol):
        '''
        Enable Regional Quotes ("R" messages) for the symbol specified.
        '''
        self.send('S,REGON,%s' % symbol)
        
    def disable_regional_quotes(self, symbol):
        '''
        Disable Regional Quotes ("R" messages) for the symbol specified.
        '''
        self.send('S,REGOFF,%s' % symbol)
    
    def enable_news(self):
        '''
        Enable Streaming News ("N" messages) to be received
        '''
        self.send('S,NEWSON')
        
    def disable_news(self):
        '''
        Disable Streaming News ("N" messages) from being received
        '''
        self.send('S,NEWSOFF')
    
    def request_stats(self):
        '''
        Request a stats message
        '''
        self.send("S,REQUEST STATS")
        
    def request_fundamental_fieldnames(self):
        '''
        Request a message containing all of the Level1 field names for Fundamental messages
        '''
        self.send("S,REQUEST FUNDAMENTAL FIELDNAMES")
    
    def request_update_fieldnames(self):
        '''
        Request a message containing all of the available Level1 field names for Update and Summary messages
        '''
        self.send('S,REQUEST ALL UPDATE FIELDNAMES')
    
if __name__ == "__main__":
    import time
    c = Level1Client()
    handler = Level1MessageHandler()
    c.set_listener('default', handler)
    try:
        with c as iqfeed:
            iqfeed.enable_news()
            iqfeed.request_stats()
            iqfeed.request_fundamental_fieldnames()
            iqfeed.request_update_fieldnames()
            iqfeed.watch('FUK')
            iqfeed.watch('DBP')
            iqfeed.enable_regional_quotes('DBP')
            
            iqfeed.unwatch('GG')
            time.sleep(5)
            
    except:
        raise