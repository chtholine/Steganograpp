import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image


# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = list(
            imdata.__next__()[:3]
            + imdata.__next__()[:3]
            + imdata.__next__()[:3]
        )

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1

            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def encode(path: str, output_path: str, message: str):
    image = Image.open(path, 'r')

    newimg = image.copy()
    encode_enc(newimg, message)

    return newimg.save(output_path)


# Decode the data in the image
def decode(path: str):
    image = Image.open(path, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = list(
            imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
        )

        binstr = ''.join('0' if (i % 2 == 0) else '1' for i in pixels[:8])
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data



class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setFixedSize(480, 630)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.setStyleSheet("")
        self.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setFixedHeight(self.height())
        self.preview = QtWidgets.QLabel(parent=self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(40, 30, 401, 291))
        self.preview.setStyleSheet("border-radius: 5px;")
        self.preview.setText("")
        self.preview.setScaledContents(False)
        self.preview.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preview.setWordWrap(False)
        self.preview.setObjectName("preview")
        self.encode_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.encode_button.setGeometry(QtCore.QRect(370, 500, 80, 31))
        self.encode_button.setObjectName("encode_button")
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 500, 331, 71))
        self.textEdit.setStyleSheet("")
        self.textEdit.setObjectName("textEdit")
        self.input_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.input_label.setGeometry(QtCore.QRect(32, 350, 131, 30))
        self.input_label.setObjectName("input_label")
        self.output_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.output_label.setGeometry(QtCore.QRect(32, 410, 161, 31))
        self.output_label.setObjectName("output_label")
        self.preview_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.preview_2.setGeometry(QtCore.QRect(30, 20, 420, 311))
        self.preview_2.setStyleSheet("font: 16pt;\n"
                                     "color: white;\n"
                                     "background-color: rgba(0, 0, 0, 0.25);\n"
                                     "border-radius: 5px\n"
                                     )
        self.preview_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preview_2.setObjectName("preview_2")
        self.decode_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.decode_button.setGeometry(QtCore.QRect(370, 540, 80, 31))
        self.decode_button.setObjectName("decode_button")
        self.browse_output = QtWidgets.QPushButton(parent=self.centralwidget)
        self.browse_output.setGeometry(QtCore.QRect(370, 440, 80, 31))
        self.browse_output.setObjectName("browse_output")
        self.browse_input = QtWidgets.QPushButton(parent=self.centralwidget)
        self.browse_input.setGeometry(QtCore.QRect(370, 380, 80, 31))
        self.browse_input.setObjectName("browse_input")
        self.output_path = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.output_path.setGeometry(QtCore.QRect(30, 440, 331, 31))
        self.output_path.setObjectName("output_path")
        self.input_path = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.input_path.setGeometry(QtCore.QRect(30, 380, 331, 31))
        self.input_path.setObjectName("input_path")
        self.handling_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.handling_label.setGeometry(QtCore.QRect(30, 590, 420, 41))
        self.handling_label.setText("")
        self.handling_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.handling_label.setObjectName("handling_label")
        self.preview_2.raise_()
        self.encode_button.raise_()
        self.textEdit.raise_()
        self.input_label.raise_()
        self.output_label.raise_()
        self.decode_button.raise_()
        self.browse_output.raise_()
        self.browse_input.raise_()
        self.output_path.raise_()
        self.input_path.raise_()
        self.preview.raise_()
        self.handling_label.raise_()
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setAutoFillBackground(False)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Connect browse button click and input path update on enter press
        self.browse_input.clicked.connect(self.browsefiles)
        self.input_path.returnPressed.connect(self.update_input_path)

        # Connect browse button click for output path
        self.browse_output.clicked.connect(self.browse_output_path)
        self.output_path.returnPressed.connect(self.update_output_path)

        # Connect encode and decode buttons
        self.encode_button.clicked.connect(self.encode_message)
        self.decode_button.clicked.connect(self.decode_message)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Steganograpp"))
        self.encode_button.setText(_translate("MainWindow", "Encode"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "hr { height: 1px; border-width: 0; }\n"
                                         "li.unchecked::marker { content: \"\\2610\"; }\n"
                                         "li.checked::marker { content: \"\\2612\"; }\n"
                                         "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Message"))
        self.input_label.setText(_translate("MainWindow", "Input image path"))
        self.output_label.setText(_translate("MainWindow", "Output image path"))
        self.preview_2.setText(_translate("MainWindow", "Image Not Found"))
        self.decode_button.setText(_translate("MainWindow", "Decode"))
        self.browse_output.setText(_translate("MainWindow", "Browse"))
        self.browse_input.setText(_translate("MainWindow", "Browse"))

    def browsefiles(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Images (*.png *.jpg *.jpeg)")
        self.input_path.setText(fname)
        self.update_image(fname)  # Call function to update image preview

    def update_input_path(self):
        # Get text from line edit and update image preview if valid path
        input_path = self.input_path.text()
        self.update_image(input_path)

    def update_output_path(self):
        # Get text from line edit
        output_path = self.output_path.text()

        # Enforce PNG extension if user doesn't provide it
        if not output_path.lower().endswith(".png"):
            output_path = f"{output_path}.png"
            self.output_path.setText(output_path)

    def browse_output_path(self):
        # Set file filter to enforce PNG files only
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Images (*.png *.jpg *.jpeg)")
        self.output_path.setText(save_path)

        # Enforce PNG extension if user doesn't provide it
        if not save_path.lower().endswith(".png"):
            self.output_path.setText(f"{save_path}.png")

    def update_image(self, path):
        try:
            self.pixmap = QPixmap(path).scaled(self.preview.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.preview.setPixmap(self.pixmap)
        except FileNotFoundError:
            # Handle case where user enters an invalid path
            self.handling_label.setText("Error: File not found")

    def encode_message(self):
        input_path = self.input_path.text()
        message = self.textEdit.toPlainText()
        output_path = self.output_path.text()

        if input_path and message:
            try:
                encode(input_path, output_path, message)
                self.handling_label.setText("Message encoded successfully!")
            except Exception as e:
                self.handling_label.setText(f"Error: {str(e)}")
        else:
            self.handling_label.setText("Error: Input path or message is empty!")

    def decode_message(self):
        if input_path := self.input_path.text():
            try:
                show_message = decode(input_path)
                self.textEdit.setPlainText(show_message)
                self.handling_label.setText("Message decoded successfully!")
            except Exception as e:
                self.handling_label.setText(f"Error: {str(e)}")
        else:
            self.handling_label.setText("Error: Input path is empty!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
