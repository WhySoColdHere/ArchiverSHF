from sys import argv, exit
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap
from ScrollLabel import ScrollLabel
from Archiver.EncoderSHF import EncoderSHF
from Archiver.DecoderSHF import DecoderSHF

'''The program supports only 2 types of files: .txt and .bin'''


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Archiver")
        self._WIDTH, self._HEIGHT = 800, 660
        self.setFixedSize(self._WIDTH, self._HEIGHT)

        self._background_image = QPixmap("images/bg_burned_better.png")

        self._background_label = QLabel(self)
        self._background_label.setPixmap(self._background_image)
        self._background_label.show()

        self._buttons_width, self._buttons_height = 40, 20
        self._buttons_stylesheet = """
            QPushButton {
                background-color: transparent;
                color: rgb(255, 255, 255);
                font-family: 'Lastri';
                font-size: 40px
            }

            QPushButton:hover {
                border: 1px solid transparent;
                border-bottom: 2px solid rgb(255, 255, 255);
            }
            """
        self._buttons = {
            QPushButton(self): self._get_buttons_settings(
                "Encode file", 50, self._HEIGHT // 2 - 100, self._encode_button_on_click
            ),
            QPushButton(self): self._get_buttons_settings(
                "Decode file", 470, self._HEIGHT // 2 - 100, self._decode_button_on_click
            )
        }
        self._encode_btn, self._decode_btn = self._buttons

        self._scroll_labels_style_sheet = """
            QLabel {
                background-color: transparent;
                color: rgb(255, 255, 255);
                font-family: 'Lastri';
                font-size: 20px;
            }
        """
        self._scroll_labels = {
            ScrollLabel(self): {'x': 39, 'y': self._HEIGHT // 2 - 30},
            ScrollLabel(self): {'x': 460, 'y': self._HEIGHT // 2 - 30}
        }
        self._input_file_scroll_label, self._output_file_scroll_label = self._scroll_labels
        self._hide_widgets(*self._scroll_labels)

        self._labels_style_sheet = """            
            QLabel {
                background-color: transparent;
                color: white;
                font-family: 'Lastri';
                font-size: 20px
            }
        """
        self._labels = {
            QLabel(self): {'x': 39, 'y': self._HEIGHT // 2 + 280},
            QLabel(self): {'x': 460, 'y': self._HEIGHT // 2 + 280}
        }
        self._original_file_label, self._processed_file_label = self._labels
        self._hide_widgets(*self._labels)

        self._customize_buttons()
        self._customize_scroll_labels()
        self._customize_labels()

    def _encode_button_on_click(self):
        filename, extend_filter = QFileDialog(self).getOpenFileName(parent=self, caption='Open file',
                                                                    filter='*.txt')
        if len(filename):
            if self._input_file_scroll_label.isHidden():
                self._show_widgets(*self._scroll_labels, *self._labels)

            if not self._is_file_empty(filename, 'r'):
                encoder_shf = EncoderSHF(filename)
                self._set_scroll_labels_text(encoder_shf.get_texts())
                self._set_labels_text(encoder_shf.get_filenames(), encoder_shf.get_file_sizes())

    def _decode_button_on_click(self):
        filename, extend_filter = QFileDialog(self).getOpenFileName(parent=self, caption='Open file',
                                                                    filter='*.bin')
        if len(filename):
            if self._input_file_scroll_label.isHidden():
                self._show_widgets(*self._scroll_labels, *self._labels)

            if not self._is_file_empty(filename, 'rb'):
                decoder_shf = DecoderSHF(filename)
                self._set_scroll_labels_text(decoder_shf.get_texts())
                self._set_labels_text(decoder_shf.get_filenames(), decoder_shf.get_file_sizes())

    def _get_buttons_settings(self, text, x, y, clicked):
        return {
            "text": text,
            "width": self._buttons_width,
            "height": self._buttons_height,
            'x': x, 'y': y,
            'clicked': clicked
        }

    def _customize_buttons(self):
        for button in self._buttons:
            button.setText(self._buttons[button]["text"])
            button.move(self._buttons[button]['x'], self._buttons[button]['y'])
            button.setStyleSheet(self._buttons_stylesheet)
            button.clicked.connect(self._buttons[button]["clicked"])

    def _customize_scroll_labels(self):
        for scroll_label in self._scroll_labels:
            scroll_label.setStyleSheet_custom(self._scroll_labels_style_sheet)
            scroll_label.move(self._scroll_labels[scroll_label]['x'], self._scroll_labels[scroll_label]['y'])

    def _set_scroll_labels_text(self, texts):
        for scroll_label, text in zip(self._scroll_labels, texts):
            scroll_label.setText_custom(text)

    def _customize_labels(self):
        for label in self._labels:
            label.resize(305, 20)
            label.setStyleSheet(self._labels_style_sheet)
            label.move(self._labels[label]['x'], self._labels[label]['y'])

    def _set_labels_text(self, filenames, file_sizes):
        for label, filename, file_size in zip(self._labels, filenames, file_sizes):
            filename_border = 15

            if len(filename) > filename_border:
                filler = ' ... '
                extension = '.' + filename.split('.')[-1]
                filename = filename[: filename_border - len(extension) - len(filler)] + filler + extension

            text = f"{filename} ----> {file_size}b"
            label.setText(text)

    @staticmethod
    def _hide_widgets(*widgets):
        for widget in widgets:
            widget.hide()

    @staticmethod
    def _show_widgets(*widgets):
        for widget in widgets:
            widget.show()

    @staticmethod
    def _is_file_empty(filename, mode: str):
        with open(filename, mode) as file:
            return True if not len(file.read()) else False


if __name__ == "__main__":
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())
