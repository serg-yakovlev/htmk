import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import redis
import event


class LoginWindow(Gtk.Window):
    
    def __init__(self):
        super().__init__(title="Mega Chat | Login")
        # event.Event(name="login")

        self.is_login = False
        self.is_password = False
        self.set_border_width(50)
        #self.set_resizable(False)
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(box)

        top_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.pack_start(top_box, True, True,0)   
        login_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        password_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        label_login = Gtk.Label(label = "Login")
        self.login = Gtk.Entry()
        self.login.connect("changed", self.on_change_login)
        login_box.pack_start(label_login,True,True,0)
        login_box.pack_start(self.login, expand = False, fill = False, padding = 5)
        top_box.pack_start(login_box, expand = False, fill = False, padding = 5)
        label_password = Gtk.Label(label = "Password")
        self.password = Gtk.Entry()
        self.password.connect("changed", self.on_change_password)
        password_box.pack_start(label_password,True,True,0)
        password_box.pack_start(self.password, expand = False, fill = False, padding = 5)
        top_box.pack_start(password_box, expand = False, fill = False, padding = 5)

        separator = Gtk.HSeparator()
        box.pack_start(separator, True, False, 5)


        # l_box = Gtk.Box()
        # p_box = Gtk.Box()


        # login_frame = Gtk.Frame(label="Login")
        # login_frame.add(login)
        # password_frame = Gtk.Frame(label="Password")
        # password_frame.add(password)        
        
        # l_box.pack_strart(login, True, False, 5)
        # p_box.pack_strart(password, True, False, 5)

        # top_box.pack_start(login_frame, False, False, 0)
        # top_box.pack_start(password_frame, False, False, 0)


        bottom_box = Gtk.Box()
        box.pack_start(bottom_box, True, True,0)

        b_box = Gtk.ButtonBox(orientation = Gtk.Orientation.VERTICAL)
        bottom_box.pack_start(b_box, False, True, 0)


        registration = Gtk.Button(label="Registration")
        registration.set_sensitive(False)
        registration.connect("clicked", self.on_registration)
        b_box.pack_start(registration, True, False, 0)

        b_space = Gtk.Alignment()
        b_box.pack_start(b_space, True, True, 0)

        c_box = Gtk.ButtonBox(orientation = Gtk.Orientation.VERTICAL)
        c_box.set_spacing(10)

        self.sign_in = Gtk.Button(label="Sign In")
        self.sign_in.connect("clicked", self.on_sign_in)
        self.sign_in.set_sensitive(False)
        c_box.pack_start(self.sign_in, True, True, 0)

        bottom_box.pack_start(c_box, True, True,0)
        
        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", Gtk.main_quit)
        c_box.pack_end(button_close, True, True, 0)



    def on_registration(self, button):
        pass

    def __check_entry(self):
        self.sign_in.set_sensitive(len(self.login.get_text())>2 and len(self.password.get_text())>2)

    @event.Event.origin("login", post = True)
    def on_sign_in(self, button):
        storage = redis.StrictRedis()
        storage.set("login", self.login.get_text())
        storage.set("password", self.password.get_text())
        storage.expire("login", 10)
        storage.expire("password", 10)
        # login = self.login.get_text()
        # password = self.password.get_text()


    def on_change_login(self, entry):
        self.__check_entry()


    def on_change_password(self, entry):
        self.__check_entry()





