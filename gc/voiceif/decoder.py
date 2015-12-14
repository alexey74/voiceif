import gobject
import pygst

import gst
import logging

gobject.threads_init()

class Decoder(object):

    def __init__(self):
        """Initialize the speech components"""
        self.suspended = False
        self.pipeline = gst.parse_launch('gconfaudiosrc ! audioconvert ! audioresample '
                  '! vader name=vad auto-threshold=true '
                  '! pocketsphinx bestpath=true fsg=basicCmd.fsg '
                    ' dict=/usr/share/pocketsphinx/model/lm/en_US/cmu07a.dic name=asr ! fakesink')
        asr = self.pipeline.get_by_name('asr')
        asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)
        asr.set_property('configured', True)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.application_message)
        self.uttid = 0

        self.pause()

    def start(self):
        if 0 : self.resume()

    def asr_partial_result(self, asr, text, uttid):
        """Forward partial result signals on the bus to the main thread."""
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def asr_result(self, asr, text, uttid):
        """Forward result signals on the bus to the main thread."""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def application_message(self, bus, msg):
        """Receive application messages from the bus."""
        if self.suspended:
            return self.pause()

        msgtype = msg.structure.get_name()
        if msgtype == 'partial_result':
            self.partial_result(msg.structure['hyp'], msg.structure['uttid'])
        elif msgtype == 'result' and msg.structure['hyp']:
            self.pause()
            self.final_result(msg.structure['hyp'], msg.structure['uttid'])


    def partial_result(self, hyp, uttid):
        logging.debug('partial: hyp: %s uttid: %s' % (hyp, uttid))



    def final_result(self, hyp, uttid):
        logging.info('final: hyp: %s uttid: %s' % (hyp, uttid))
        self.uttid = long(uttid)
        #self.resume()

    def pause(self):
        logging.info('pausing decoder')
        self.paused = True
        self.pipeline.set_state(gst.STATE_PAUSED)

    def resume(self):
        if self.suspended : return
        logging.info('resuming decoder')
        self.paused = False
        self.pipeline.set_state(gst.STATE_PLAYING)


