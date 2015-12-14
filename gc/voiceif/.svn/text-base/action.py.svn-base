
import time, sys, os, random, logging
import wnck

from speaker import Speaker

__VERSION__ = '0.1'

UNKNOWN = [ 'Request unknown',
     'Please restate request', 'Request not understood' ]


class ActionHandler(Speaker):

    def __init__(self):
        Speaker.__init__(self)
        self.scr =  wnck.screen_get_default()
        self.state = None

    def start(self):
        pass

    def ready(self):
        pass

    def handle(self, text, cmdl):
        logging.info('[%s%s]: %s cmd: %s' % ('L' if self.listening else 'S',
            ' sil' if self.silent else '', text, cmdl))
        k = 'a_' + cmdl[0]

#        if self.state: # ignore requests until choice made on state
#            self.state(*cmdl)

        if hasattr(self, k):
           if getattr(self, k)(*cmdl):
                self.ready()
        elif len(cmdl) > 1 and hasattr(self, 'a_' + '_'.join(cmdl)):
           if getattr(self, 'a_' + '_'.join(cmdl))():
                self.ready()

        else:
            self.unknown_request(text)

    def unknown_request(self, text):
            self.beep('227', random.choice(UNKNOWN))


    def a_time(self, *args):
        self.speak(time.strftime('The time is %H hours %M minutes' ), True)

    def a_date(self, *args):
        self.speak(time.strftime('The date is %A %B %d' ), True)

    def a_minimize_window(self, *args):
        self.scr.get_active_window().minimize()
        return True

    def a_show_desktop(self, *args):
        self.scr.toggle_showing_desktop(True)
        return True

    def a_hide_desktop(self, *args):
        self.scr.toggle_showing_desktop(False)
        return True

    def a_silent_mode(self, *args):
        self.beep('210')
        self.silent = True
        return True

    def a_loud_mode(self, *args):
        self.silent = False
        self.beep('201')
        return True

    def a_respond(self, *args):
        self.beep('201', 'VI version %s ready' % __VERSION__, True)

    def a_affirmative(self, *a):
        if self.state :
            self.state('affirmative')
        return True

    def a_negative(self, *a):
        self.state = None
        self.speak('Request cancelled')

    def a_suspend_voice_interface(self, *a):
        self.state = self.a_suspend_voice_interface
        if 'affirmative' in a :
            self.beep('231')
            self.pause()
            self.state = None
            self.suspended = True
        else:
            self.speak('Please confirm request to suspend the voice interface')
            self.listening = True

    def a_sleep(self, *a):
        self.beep('212')
        os.system('xset dpms force off')
        return True

    def a_resume(self, *a):
        self.beep('210')
        os.system('xset dpms force on')
        return True

    def a_shutdown_voice_interface(self, *a):
        self.state = self.a_shutdown_voice_interface
        if 'affirmative' in a :
            self.state = None
            self.ready=self.quit
            self.speak('Voice interface shutting down. Goodbye!')

        else:
            self.speak('Please confirm request to shutdown the voice interface')
            self.listening = True

    def a_lock_screen(self, *a):
        os.system('gnome-screensaver-command -l')
        return True

    def a_status(self, *a):
        self.speak('%s listening, %s silent, %u utterances processed' % ('' if self.listening else 'not',
            '' if self.silent else 'not', self.uttid))

