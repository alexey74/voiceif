import logging, time

from espeak import espeak
import gtk

class ESpeakerDirect(object):
    def __init__(self):
        self.silent = False
        espeak.set_SynthCallback(self._e_eventCB)

    def _e_eventCB(self, event, pos, length):

        gtk.gdk.threads_enter()


        if event == espeak.core.event_WORD:
            pass

        if event == espeak.event_MSG_TERMINATED:
            logging.info('espeak evt: %s' % event)
            self.ready()

        gtk.gdk.threads_leave()

        return True

    def start(self):
        pass

    def speak(self, text):
        if not self.silent:
            espeak.synth(text)

    def ready(self):
        pass


import gst

class ESpeakerGST(object):
    def gstmessage_cb(self, bus, message, pipe):
         if message.type in (gst.MESSAGE_EOS, gst.MESSAGE_ERROR):
             pipe.set_state(gst.STATE_NULL)
             logging.info('done speaking')
             self.ready()

    def __init__(self):
        self.silent = False


    def start(self):
        pass

    def speak(self, text, anyway=False):
        if not self.silent or anyway:
             logging.info('speaking: %s' % text)
             pipeline = 'espeak voice=en-us name=src ! autoaudiosink'
             self.pipe = pipe = gst.parse_launch(pipeline)
             pipe.get_by_name('src').set_property('text', text)

             bus = pipe.get_bus()
             bus.add_signal_watch()
             bus.connect('message', self.gstmessage_cb, pipe)

             pipe.set_state(gst.STATE_PLAYING)
        else:
            self.ready()

    def ready(self):
        pass


ESpeaker = ESpeakerGST

class Beeper(object):
    defbeep = '201'
    defdir = 'sounds/'

    def __init__(self):
        self.silent = False

    def gstmessage_cb_beep(self, bus, message, tt):
        if message.type in (gst.MESSAGE_EOS, gst.MESSAGE_ERROR):
            text, anyway, p = tt
            p.set_state(gst.STATE_NULL)
            logging.info('done beeping')

            if text:
                self.speak(text, anyway)
            else:
                self.ready()

    def beep(self, snd='201', text='', anyway=False):
       if not self.silent or anyway:
            p = self.pipe_beep = gst.parse_launch('filesrc name=fsrc '
                '! decodebin ! audioconvert ! audioresample ! autoaudiosink' )
            fsrc = self.pipe_beep.get_by_name('fsrc')
            fsrc.set_property('location', self.defdir + snd + '.wav')

            bus = self.pipe_beep.get_bus()
            bus.add_signal_watch()
            bus.connect('message', self.gstmessage_cb_beep, (text, anyway, p))

            self.pipe_beep.set_state(gst.STATE_PLAYING)


class Speaker(ESpeaker, Beeper):
    def __init__(self):
        ESpeaker.__init__(self)
        Beeper.__init__(self)

