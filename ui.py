
import pygtk, logging
pygtk.require('2.0')
import gtk
import pynotify

gtk.gdk.threads_init()

class UI(object):
    def __init__(self):
        self.window = gtk.Window()
        self.sticon = gtk.StatusIcon()
        self.sticon.set_from_stock(gtk.STOCK_MEDIA_PLAY)

        self.notif = pynotify.Notification('Voice interface ready')
        self.notif.attach_to_status_icon(self.sticon)

        self.menu = menu = gtk.Menu()

        self.m_pause = menuItem = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PAUSE)
        menuItem.connect('activate', self.pause_cb, self.sticon)
        menuItem.set_sensitive(not self.paused)
        menu.append(menuItem)

        self.m_play = menuItem = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PLAY)
        menuItem.connect('activate', self.resume_cb, self.sticon)
        menuItem.set_sensitive(self.paused)
        menu.append(menuItem)

        menu.append(gtk.SeparatorMenuItem())

        menuItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        menuItem.connect('activate', self.prefs_cb, self.sticon)
        menu.append(menuItem)

        menu.append(gtk.SeparatorMenuItem())

        menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menuItem.connect('activate', self.about_cb, self.sticon)
        menu.append(menuItem)

        menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menuItem.connect('activate', self.quit_cb, self.sticon)
        menu.append(menuItem)


        self.sticon.set_tooltip("Desktop Voice Interface")
        self.sticon.connect('popup-menu', self.popup_menu_cb, menu)
        self.sticon.set_visible(True)


    def quit_cb(self, widget, data = None):
        logging.info('Quit via menu')
        if data:
            data.set_visible(False)
        self.quit()

    def quit(self):
        logging.info('Quitting...')
        gtk.main_quit()



    def about_cb(self, widget, data = None):
        pass

    def prefs_cb(self, widget, data = None):
        pass

    def toggle_pp(self):
        try:
            self.m_play.set_sensitive(self.paused)
            self.m_pause.set_sensitive(not self.paused)
        except AttributeError:
            pass

    def pause_cb(self, widget, data = None):
        self.pause()

    def resume_cb(self, widget, data = None):
        self.resume()

    def pause(self, *args):
        logging.info ('ui pause')
        self.toggle_pp()

    def resume(self, *args):
        logging.info ('ui resume')
        self.suspended = False
        self.toggle_pp()

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)
        elif button == 1:
            if self.paused:
                self.resume()
            else:
                self.pause()

    def main(self):
        gtk.main()

    def notify(self, text):
        return ###
        self.notif.update(text)
        self.notif.show()



