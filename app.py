from PySide6 import QtGui, QtWidgets, QtCore

import _qrcode


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 500)
        self.setWindowTitle("pyQRCode")
        self.choice_color = ("White", "Silver", "Gray", "Black", "Red", "Maroon",
                             "Yellow", "Olive", "Lime", "Green", "Aqua", "Teal",
                             "Blue", "Navy", "Fuchsia", "Purple")
        self.choice_style = ("default", "rounded",
                             "square", "Vbar", "Hbar", "circle")
        self.choice_mask = ("default", "RadialGradiant", "SquareGradiant",
                            "HorizontalGradiant", "VerticalGradiant")
        self.setup_ui()

    def setup_ui(self):
        self.create_layout()
        self.create_widgets()
        self.add_widget_to_layout()
        self.setup_connexions()
        self.css()
        
        self.btn_edge_color.setEnabled(False)
        self.btn_image_selector.chk = False

    def create_layout(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.left_layout = QtWidgets.QGridLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

    def create_widgets(self):
        # LEFT LAYOUT
        self.lbl_qrcode_size = QtWidgets.QLabel("QRCode details (1, 40)")
        self.le_qrcode_size = QtWidgets.QLineEdit()
        self.le_qrcode_size.setText("1")

        self.lbl_box_size = QtWidgets.QLabel("Box size (1, 100)")
        self.le_box_size = QtWidgets.QLineEdit()
        self.le_box_size.setText("10")

        self.lbl_border_size = QtWidgets.QLabel("Border size (1, 20)")
        self.le_border_size = QtWidgets.QLineEdit()
        self.le_border_size.setText("2")

        self.lbl_color_choice = QtWidgets.QLabel(
            "Color choice: ", objectName="special_label")
        self.lbl_color_choice.setAlignment(QtCore.Qt.AlignCenter)

        self.btn_qrcode_color = QtWidgets.QPushButton(
            "QRCode", objectName="special_button")
        self.btn_background_color = QtWidgets.QPushButton(
            "Background", objectName="special_button")
        self.btn_edge_color = QtWidgets.QPushButton(
            "Edge", objectName="special_button")

        self.lbl_module_drawer = QtWidgets.QLabel(
            "QRCode Style :", objectName="special_label")
        self.cb_module_drawer = QtWidgets.QComboBox()
        self.cb_module_drawer.addItems(self.choice_style)
        self.lbl_module_drawer.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_mask_color = QtWidgets.QLabel(
            "Color Mask: ", objectName="special_label")
        self.cb_mask_color = QtWidgets.QComboBox()
        self.cb_mask_color.addItems(self.choice_mask)
        self.lbl_mask_color.setAlignment(QtCore.Qt.AlignCenter)
        
        self.lbl_image_selector = QtWidgets.QLabel("Select the image - center of the qrcode\ndefault none")
        self.btn_image_selector = QtWidgets.QPushButton("Add")

        self.te_data = QtWidgets.QTextEdit()
        self.te_data.setPlaceholderText("QRCode content")

        self.btn_generate = QtWidgets.QPushButton("Generate")

        # RIGHT LAYOUT
        self.lbl_picture = QtWidgets.QLabel("", objectName="qrcode")
        self.lbl_picture.setFixedWidth(400)

    def add_widget_to_layout(self):
        # LEFT LAYOUT
        self.left_layout.addWidget(self.lbl_qrcode_size, 0, 0, 1, 2)
        self.left_layout.addWidget(self.le_qrcode_size, 0, 2, 1, 2)

        self.left_layout.addWidget(self.lbl_box_size, 1, 0, 1, 2)
        self.left_layout.addWidget(self.le_box_size, 1, 2, 1, 2)

        self.left_layout.addWidget(self.lbl_border_size, 2, 0, 1, 2)
        self.left_layout.addWidget(self.le_border_size, 2, 2, 1, 2)

        self.left_layout.addWidget(self.lbl_color_choice, 3, 0, 1, 4)

        self.left_layout.addWidget(self.btn_qrcode_color, 4, 0, 1, 2)

        self.left_layout.addWidget(self.btn_background_color, 4, 1, 1, 2)

        self.left_layout.addWidget(self.btn_edge_color, 4, 2, 1, 2)

        self.left_layout.addWidget(self.lbl_module_drawer, 5, 0, 1, 2)
        self.left_layout.addWidget(self.lbl_mask_color, 5, 2, 1, 2)
        self.left_layout.addWidget(self.cb_module_drawer, 6, 0, 1, 2)
        self.left_layout.addWidget(self.cb_mask_color, 6, 2, 1, 2)
        
        self.left_layout.addWidget(self.lbl_image_selector, 7, 0, 1, 2)
        self.left_layout.addWidget(self.btn_image_selector, 7, 2, 1, 2)

        self.left_layout.addWidget(self.te_data, 8, 0, 1, 4)

        self.left_layout.addWidget(self.btn_generate, 9, 0, 1, 4)

        # RIGHT LAYOUT
        self.right_layout.addWidget(self.lbl_picture)

    def css(self):
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())

    def setup_connexions(self):
        self.btn_background_color.clicked.connect(
            lambda x: self.get_color("background_color"))
        self.btn_edge_color.clicked.connect(
            lambda x: self.get_color("edge_color"))
        self.btn_qrcode_color.clicked.connect(
            lambda x: self.get_color("qrcode_color"))
        self.btn_generate.clicked.connect(self.generate_qrcode)
        self.cb_mask_color.currentTextChanged.connect(self.show_params)
        self.btn_image_selector.clicked.connect(self.get_center_image)
        
    def get_center_image(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        images_dir = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.PicturesLocation)
        file_dialog.setDirectory(images_dir)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.img_center = (str(file_dialog.selectedUrls()[0])).split("//")[1][0:-2]
            self.btn_image_selector.chk = True

    def get_color(self, button):
        color_dialog = QtWidgets.QColorDialog(self)
        self.selected_color = color_dialog.getColor().getRgb()[0:3]
        selected_color = QtGui.QColor(*self.selected_color)
        
        if button == "background_color":
            self.btn_background_color.setStyleSheet(
                "border-left: 10px solid %s" % selected_color.name())
            self.btn_background_color.value = self.selected_color
        elif button == "edge_color":
            self.btn_edge_color.setStyleSheet(
                "border-left: 10px solid %s" % selected_color.name())
            self.btn_edge_color.value = self.selected_color
        else:
            self.btn_qrcode_color.setStyleSheet(
                "border-left: 10px solid %s" % selected_color.name())
            self.btn_qrcode_color.value = self.selected_color
            
    def show_params(self):
        
        def set_text(font, edge, btnEdge=True):
            self.btn_qrcode_color.setText(font)
            self.btn_edge_color.setText(edge)
            self.btn_edge_color.setEnabled(btnEdge)
        
        current_item = self.cb_mask_color.currentText()
             
        if current_item == "default":
            set_text("QRCode", "Edge", False)
            
        elif current_item in ["RadialGradiant", "SquareGradiant"]:
            set_text("QRCode", "Edge")
            
        elif current_item == "VerticalGradiant":   
            set_text("Top", "Bottom")   
            
        elif current_item == "HorizontalGradiant":
            set_text("Left", "Right")
            
    def generate_qrcode(self):
        
        def chk_isdigit(item, min: int, max: int):
            item = item.text()
            if item.isdigit() and (int(item) <= max and int(item) >= min):
                return int(item) 
            
        data = self.te_data.toPlainText()

        try:
            qr_color = self.btn_qrcode_color.value
        except AttributeError:
            qr_color = (0, 0, 0)

        try:
            bg_color = self.btn_background_color.value
        except AttributeError:
            bg_color = (255, 255, 255)

        try:
            edge_color = self.btn_edge_color.value
        except AttributeError:
            edge_color = (255, 255, 255)
            
        qr_size = chk_isdigit(self.le_qrcode_size, 1, 40)
        box_size = chk_isdigit(self.le_box_size, 1, 100)
        border = chk_isdigit(self.le_border_size, 0, 20)

        img = _qrcode.CustomQrCode(data=data, qr_color=qr_color, bg_color=bg_color,
                             edge_color=edge_color, qr_size=qr_size, box_size=box_size, border=border)
        
        module_drawer = self.cb_module_drawer.currentText()
        color_mask = self.cb_mask_color.currentText()
        
        if not self.btn_image_selector.chk:
            self.img_center = ""                 
        img.create(mod=module_drawer, color_mask=color_mask, img_path=self.img_center)
        
        pixmap = QtGui.QPixmap("output/qrcode.png")
        pixmap = pixmap.scaledToWidth(300)
        self.lbl_picture.setPixmap(pixmap)
                          
                          
app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
