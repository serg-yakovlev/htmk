import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
import chat
import login
import redis
import  json
import os
import event

HOST = "127.0.0.1"
PORT = 5000


class ChatWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Mega Chat | Login")
        event.Event(name="login",callback=self.regy_date)
        self.login_win = login.LoginWindow()
        self.login_win.show_all()
        self.connection = None
        self.__interface()

    def __interface(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 600)

        master_box = Gtk.Box()
        master_box.set_spacing(5)
        self.add(master_box)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_box.set_size_request(200, -1)
        master_box.pack_start(left_box, False, True, 0)
        separator = Gtk.VSeparator()
        master_box.pack_start(separator, False, False, 0)

        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        master_box.pack_start(center_box, True, True, 0)
        separator = Gtk.VSeparator()
        master_box.pack_start(separator, False, False, 0)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_size_request(200, -1)
        master_box.pack_start(right_box, False, True, 0)

        pict = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename=os.path.join(
                 os.path.dirname(os.path.abspath(__file__)),
                 "Avatar.png"
                 ),
        width=150,
        height=150,
        preserve_aspect_ratio=True)

        avatar = Gtk.Image.new_from_pixbuf(pict)

        # avatar = Gtk.Image()
        # avatar.set_from_file(
        #     os.path.join(
        #         os.path.dirname(os.path.abspath(__file__)),
        #         "avatar.jpg"
        #         )
        #     )
        # avatar.set_size_request(50,50)

        left_box.pack_start(avatar, False, True, 5)
        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 5)

        user_label = Gtk.Label(label = "User name")
        left_box.pack_start(user_label, False, True, 0)
        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 5)

        l_space = Gtk.Alignment()
        left_box.pack_start(l_space, True, True, 5)

        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 5)

        b_box = Gtk.ButtonBox()
        b_box.set_spacing(5)
        left_box.pack_start(b_box, False, False, 5)

        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, False, 5)

        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", Gtk.main_quit)
        b_box.pack_start(close_button, True, True, 5)

        scroll_box = Gtk.ScrolledWindow()
        scroll_box.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        center_box.pack_start(scroll_box, True, True, 5)

        self.chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll_box.add(self.chat_box)
        separator = Gtk.HSeparator()
        center_box.pack_start(separator, False, False, 5)


#        output_message = Gtk.Frame()

        send_box = Gtk.Box()
        send_box.set_spacing(5)
        center_box.pack_start(send_box, False, True,  5)

        separator = Gtk.HSeparator()
        center_box.pack_start(separator, False, False, 5)

        smile_button = Gtk.Button(label = ":-)")
        send_box.pack_start(smile_button, False, False, 0)

        message_entry = Gtk.Entry()
        send_box.pack_start(message_entry, True, True, 0)

        send_button = Gtk.Button(label = "send")
        send_box.pack_start(send_button, False, False, 0)

        favorite_label = Gtk.Label(label = "Favorites")
        right_box.pack_start(favorite_label, False, False, 0)

#        self.show_all()

        # test_input = {
        # "message": ("Этот модуль считается устаревшим. "
        #     "Он будет по-прежнему поддерживаться и сохранять стабильность "
        #     "API/ABI на всём протяжении серии GNOME 2.x, но мы не советуем "
        #     "использовать его в новых приложениях, если только вам "
        #     "не требуются возможности, которые ещё не перенесены "
        #     "в другие модули."
        #     ),
        # "user": "vasia"
        # }

        # test_output = {
        # "message": ("Указатель на пиксельные данные pixbuf. "
        #     "Пожалуйста, смотрите раздел о данных изображения для "
        #     "получения информации о том, как данные пикселей "
        #     "хранятся в памяти.Эта функция будет вызывать неявную "
        #     "копию данных pixbuf, если pixbuf был создан из "
        #     "данных только для чтения. "
        #     ),
        # "user": "User"
        # }

        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)

    def __add_message_box(self, data, input=True):
        message = Gtk.Frame()
        self.chat_box.pack_start(message, False, True,  5)

        pict = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        filename=os.path.join(
                 os.path.dirname(os.path.abspath(__file__)
                ),
                 f".contacts/{data['user']}.png" if input else "Avatar.png"
                ), 
        width=100, 
        height=100, 
        preserve_aspect_ratio=True)
        avatar = Gtk.Image.new_from_pixbuf(pict)
        message_box = Gtk.Box()
        message.add(message_box)
        text_label = Gtk.Label()
        text_label.set_markup(data['message'])
        text_label.set_selectable(True)
        text_label.set_line_wrap(True)
        if input:
            message_box.pack_start(avatar, True, False,  5)
        else:
            message_box.pack_end(avatar, True, False,  5)
            text_label.set_justify(Gtk.Justification.RIGHT)
        message_box.pack_start(text_label, True, False,  5)

    def regy_date(self, *args, **kwargs):
        self.login_win.hide()
        storage = redis.StrictRedis()
        try:
            self.login_win = storage.get("login")
            self.password = storage.get("password")
        except redis.RedisError:
            print("No data")
            Gtk.main_quit()
        else:
            self.__create_connection()
            #self.show_all()


    def __create_connection(self):
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # self.connection.setblocking(0)
            self.connection.connect((HOST,PORT))
            result = self.connection.reqv(2048)
            data = json.loads(result.decode("utf-8"))
            if data.get("status") != "OK":
                print(data.get("message"))
                Gtk.main_quit()
            else:
                data = json.dumps({"login": self.login, "password": self.password})
                self.connection.send(data.encode("utf-8"))
                self__run()


    def run(self):
            # self.epoll = select.epoll()
            # self.epoll.register(self.sock.fileno(), select.EPOLLIN)
        pass

if __name__ == '__main__':

    #print(dir(Gtk.Entry.connect.__name__))
    win = ChatWindow()
    win.connect("destroy", Gtk.main_quit)
    #win.show_all()
    Gtk.main()