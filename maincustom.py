import ctypes
import tkinter
import customtkinter
from loguru import logger
from textcrypt import gettextcrypt

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{600}x{400}+{1200}+{100}")
        self.title("Encoder/decoder text processor")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.logo_label = customtkinter.CTkLabel(self, text="Enter text for encode or decode:",
                                                 font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.textbox = customtkinter.CTkTextbox(self, font=customtkinter.CTkFont(size=12))
        self.textbox.grid(row=1, column=0, sticky="nsew")
        self.textbox.bind('<Control-KeyPress>', command=self.keys_event)

        self.button = customtkinter.CTkButton(self, width=500, text="Encode / Decode", command=self.button_event)
        self.button.grid(row=2, column=0, padx=10, pady=10)

    def button_event(self):
        text = self.textbox.get(1.0, tkinter.END)
        text_crypt = gettextcrypt(text).strip('\n')
        self.textbox.delete(1.0, tkinter.END)
        self.textbox.insert(1.0, text_crypt)
        logger.info(text)

    @staticmethod
    def is_ru_lang_keyboard() -> bool:
        u = ctypes.windll.LoadLibrary('user32.dll')
        pf = getattr(u, 'GetKeyboardLayout')
        return hex(pf(0)) == '0x4190419'

    def keys_event(self, event):
        if self.is_ru_lang_keyboard():
            if event.keycode == 86:
                event.widget.event_generate("<<Paste>>")
            elif event.keycode == 67:
                event.widget.event_generate("<<Copy>>")
            elif event.keycode == 88:
                event.widget.event_generate("<<Cut>>")
            elif event.keycode == 65535:
                event.widget.event_generate("<<Clear>>")
            elif event.keycode == 65:
                event.widget.event_generate("<<SelectAll>>")
        logger.debug(f'Code: {event.keycode}, char ')


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
