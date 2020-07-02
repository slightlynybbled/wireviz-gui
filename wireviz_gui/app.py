import logging
from io import BytesIO, StringIO
import tkinter as tk

from PIL import Image, ImageTk
from wireviz.wireviz import parse

from wireviz_gui._base import BaseFrame


class Application(tk.Tk):
    def __init__(self, loglevel=logging.INFO, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        super().__init__()

        r = 0
        self._title_frame = TitleFrame(self)
        self._title_frame.grid(row=r, column=0, sticky='ew')

        r += 1
        self._io_frame = InputOutputFrame(self)
        self._io_frame.grid(row=r, column=0, sticky='ew')

        self.mainloop()


class TitleFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        r = 0
        tk.Label(self, text='WireViz GUI', **self._heading)\
            .grid(row=r, column=0, sticky='ew')


class InputOutputFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._text_entry_frame = TextEntryFrame(self, on_update_callback=self._update)
        self._text_entry_frame.grid(row=0, column=0, sticky='ew')

        self._harness_frame = HarnessFrame(self)
        self._harness_frame.grid(row=0, column=0, sticky='ew')

    def _update(self):
        """
        This is where the data is read from the text entry and parsed into an image

        :return:
        """
        f_in = StringIO(self._text_entry_frame.get())

        data = parse(f_in, return_types='png')
        photo = ImageTk.PhotoImage(data=data)

        self._harness_frame\
            .update_image(photo_image=photo)


class TextEntryFrame(BaseFrame):
    def __init__(self, parent, on_update_callback: callable = None, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._on_update_callback = on_update_callback

        self._text = tk.Text()
        self._text.grid(row=0, column=0, sticky='news')
        self._text.bind('<Control-l>', lambda _: self._updated())

    def associate_callback(self, on_update_callback: callable):
        self._on_update_callback = on_update_callback

    def _updated(self):
        if self._on_update_callback is not None:
            self._on_update_callback()

    def get(self):
        return self._text.get('1.0', 'end')


class HarnessFrame(BaseFrame):
    def __init__(self, parent, loglevel=logging.INFO):
        super().__init__(parent, loglevel=loglevel)

        self._label = tk.Label(self, text='(no harness defined)')
        self._label.grid(row=0, column=0, sticky='ew')
        self._pi = None  # photoimage data

    def update_image(self, photo_image: ImageTk.PhotoImage):
        self._pi = photo_image
        self._label.config(
            text=None,
            image=photo_image
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Application()
