import ctypes
import sys
import os
import configparser
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from loguru import logger
from textcrypt import gettextcrypt, set_password, generate_password


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{600}x{400}+{1200}+{100}")
        self.title("Encoder/decoder text processor")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        self.style.theme_use('vista')
        logger.debug(self.style.theme_names())

        self.style.configure('TLabel', font=('Arial', 16))
        self.style.configure('TButton', font=('Arial', 16))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.enter_label = ttk.Label(self, text="Enter text for encode or decode:")
        self.enter_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.frame_text = tk.Frame()
        self.scroll = tk.Scrollbar(self.frame_text)

        self.textbox = tk.Text(self.frame_text, yscrollcommand=self.scroll.set, font=Font(family='Arial', size=10))
        self.textbox.bind('<Control-KeyPress>', self.keys_event)

        self.scroll.config(command=self.textbox.yview)
        self.textbox.pack(side=tk.TOP, fill="both", expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_text.grid(row=1, column=0, sticky="nsew")

        self.button = ttk.Button(self, width=500, text="Encode / Decode", command=self.button_event)
        self.button.grid(row=2, column=0, padx=10, pady=10)

    def button_event(self):
        text = self.textbox.get(1.0, tk.END)
        text_crypt = gettextcrypt(text).strip('\n')
        self.textbox.delete(1.0, tk.END)
        self.textbox.insert(1.0, text_crypt)
        self.clipboard_clear()
        self.clipboard_append(text_crypt)
        logger.info(text)

    @staticmethod
    def is_ru_lang_keyboard() -> bool:
        if sys.platform == 'win32':
            u = ctypes.windll.LoadLibrary('user32.dll')
            pf = getattr(u, 'GetKeyboardLayout')
            return hex(pf(0)) == '0x4190419'
        else:
            # TODO: GetKeyboard state for linux systems

            return False

    @staticmethod
    def keys_event(event):
        event_list = {86: "<<Paste>>", 67: "<<Copy>>", 88: "<<Cut>>", 76: "<<Clear>>", 65: "<<SelectAll>>"}
        # Hot key hack for russian keyboard
        # Ctrl - (state = 12) 86 - V, 67 - C, 88 - X, 76 - L, 65 - A
        if event.state == 12 and event.keycode in (86, 67, 88, 76, 65):
            event.widget.event_generate(event_list[event.keycode])
            return "break"

        logger.debug(f'Code: {event.keycode}, char {event.char}')


def set_save_password():
    _file_config = os.path.splitext(os.path.basename(__file__))[0] + '.ini'
    _section = 'Passwords'
    _key_password = 'password'

    conf = configparser.ConfigParser()
    conf.read(_file_config)
    if not (conf.has_option(_section, _key_password) and
            set_password(conf.get(_section, _key_password))):
        psw = generate_password()
        set_password(psw)
        if not conf.has_section(_section):
            conf.add_section(_section)
        conf.set(_section, _key_password, psw)
        with open(_file_config, 'w') as file:
            conf.write(file)


def main():
    set_save_password()
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
