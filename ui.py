from sys import argv, exit
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap
from ScrollLabel import ScrollLabel
from Archiver.Archiver import Archiver

'''The program supports only 2 types of files: .txt and .bin'''


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Archived")
        self._WIDTH, self._HEIGHT = 800, 660
        self.setFixedSize(self._WIDTH, self._HEIGHT)

        self._background_image = QPixmap("images/bg.jpg")

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
                color: white;
                font-family: 'Lastri';
                font-size: 20px
            }
        """
        self._scroll_labels = {
            ScrollLabel(self): {'x': 39, 'y': self._HEIGHT // 2 - 30},
            ScrollLabel(self): {'x': 460, 'y': self._HEIGHT // 2 - 30}
        }
        self._input_file_scroll_label, self._output_file_scroll_label = self._scroll_labels
        self._input_file_scroll_label.hide()
        self._output_file_scroll_label.hide()

        self._labels_style_sheet = """            
            QLabel {
                background-color: transparent;
                color: white;
                font-family: 'Lastri';
                font-size: 10px
            }
        """
        self._labels = {
            QLabel(self): {'x': 39, 'y': self._HEIGHT // 2 - 330},
            QLabel(self): {'x': 460, 'y': self._HEIGHT // 2 - 330}
        }
        self._original_file_size_label, self._processed_file_size_label = self._labels
        self._original_file_size_label.hide()
        self._processed_file_size_label.hide()

        self._customize_buttons()
        self._customize_scroll_labels()
        self._customize_labels()

    def _encode_button_on_click(self):
        filename, extend_filter = QFileDialog(self).getOpenFileName(parent=self, caption='Open file',
                                                                    filter='*.txt')
        if len(filename) == 0:
            print("Alert! Filename doesn't exists")
        else:
            if self._input_file_label.isHidden():
                self._show_scroll_labels()

            data = Archiver.encode_shf(filename)
            print(data)
            # self._set_scroll_labels_text(*data[:2])
            # self._set_labels_text(*data[2:])

    def _decode_button_on_click(self):
        filename, extend_filter = QFileDialog(self).getOpenFileName(parent=self, caption='Open file',
                                                                    filter='*.bin')
        if len(filename) == 0:
            print("Alert! Filename doesn't exists")
        else:
            if self._input_file_label.isHidden():
                self._show_labels()

            data = Archiver.decode_shf(filename)
            self._set_scroll_labels_text(*data[:2])
            self._set_labels_text(*data[2:])

    def _get_buttons_settings(self, text, x, y, clicked):
        return {
            "text": text,
            "width": self._buttons_width,
            "height": self._buttons_height,
            'x': x, 'y': y,
            'clicked': clicked
        }

    def _customize_labels(self):
        for label in self._labels:
            label.setStyleSheet(self._labels_style_sheet)
            label.move(self._labels[label]['x'], self._labels[label]['y'])

    def _set_labels_text(self, *texts):
        for label, text in zip(self._labels, texts):
            label.setText(text)

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

    def _show_scroll_labels(self):
        for scroll_label, label in zip(self._scroll_labels, self._labels):
            scroll_label.show()
            label.show()

    def _set_scroll_labels_text(self, *texts):
        for scroll_label, text in zip(self._scroll_labels, texts):
            scroll_label.setText_custom(text)


if __name__ == "__main__":
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec_())
