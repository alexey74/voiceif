#!/usr/bin/env python

'''
Desktop Voice Interface
'''
__VERSION__ = '0.1'

import sys, random, os, time, traceback
from ui import UI
from action import ActionHandler
from decoder import Decoder
from speaker import Speaker

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

INTRO=['computer listen']
START=['computer']
STANDBY=[ 'standby' ]

class App(UI, Decoder, ActionHandler):
    def __init__(self):
        Decoder.__init__(self)
        ActionHandler.__init__(self)
        UI.__init__(self)
        self.listening = False


    def main(self):
        Decoder.start(self)
        ActionHandler.start(self)

        self.beep('201', 'Voice interface ready.')
        UI.main(self)

    def final_result(self, hyp, uttid):
        Decoder.final_result(self, hyp, uttid)
        self.handle(hyp)

    def handle(self, text):
        listen_once = False

        text = text.strip().lower()
        cmdl = text.split()

        if cmdl :
            try :
                if text in INTRO:
                    self.beep()
                    self.listening = True

                else:
                    if cmdl[0] in START:
                        cmdl = cmdl[1:]
                        listen_once = True

                    if cmdl:

                        if self.listening or listen_once:
                            if cmdl[0] in STANDBY :
                                self.listening=False
                                self.beep('211')

                            else:
                                self.notify('You said: %s' % text)
                                super(App,self).handle(text, cmdl)

                        else:
                            if cmdl[0] in STANDBY :
                                self.beep('211')
                            else:
                                self.ready()
                    else:
                        self.beep('203')


            except Exception, e:
                logging.error('Exception in handle(): %s' %e)
                traceback.print_exc()
                self.beep('215', 'Sorry, internal error.')

            logging.info ('[%s]: %s' % ('!' if self.listening or listen_once else '.', text))

    def ready(self):
        self.resume()

    def pause(self, *args):
        Decoder.pause(self)
        UI.pause(self)

    def resume(self, *args):
        Decoder.resume(self)
        UI.resume(self)


def compile_gram():
    os.system('make')


if __name__ == '__main__':
    compile_gram()
    app = App()
    app.main()




