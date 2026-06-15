from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(50, 20, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        
        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setGeometry(QtCore.QRect(420, 20, 120, 30))
        self.btn_gen_keys.setObjectName("btn_gen_keys")
        
        self.lbl_plain = QtWidgets.QLabel(self.centralwidget)
        self.lbl_plain.setGeometry(QtCore.QRect(50, 70, 80, 20))
        self.lbl_plain.setObjectName("lbl_plain")
        
        self.txt_plain_text = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_plain_text.setGeometry(QtCore.QRect(50, 100, 300, 120))
        self.txt_plain_text.setObjectName("txt_plain_text")
        
        self.lbl_cipher = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cipher.setGeometry(QtCore.QRect(50, 240, 80, 20))
        self.lbl_cipher.setObjectName("lbl_cipher")
        
        self.txt_cipher_text = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_cipher_text.setGeometry(QtCore.QRect(50, 270, 300, 120))
        self.txt_cipher_text.setObjectName("txt_cipher_text")
        
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(80, 400, 100, 30))
        self.btn_encrypt.setObjectName("btn_encrypt")
        
        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(200, 400, 100, 30))
        self.btn_decrypt.setObjectName("btn_decrypt")
        
        self.lbl_info = QtWidgets.QLabel(self.centralwidget)
        self.lbl_info.setGeometry(QtCore.QRect(400, 70, 80, 20))
        self.lbl_info.setObjectName("lbl_info")
        
        self.txt_info = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_info.setGeometry(QtCore.QRect(400, 100, 300, 120))
        self.txt_info.setObjectName("txt_info")
        
        self.lbl_signature = QtWidgets.QLabel(self.centralwidget)
        self.lbl_signature.setGeometry(QtCore.QRect(400, 240, 80, 20))
        self.lbl_signature.setObjectName("lbl_signature")
        
        self.txt_sign_sent = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_sign_sent.setGeometry(QtCore.QRect(400, 270, 300, 120))
        self.txt_sign_sent.setObjectName("txt_sign_sent")
        
        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(450, 400, 100, 30))
        self.btn_sign.setObjectName("btn_sign")
        
        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(570, 400, 100, 30))
        self.btn_verify.setObjectName("btn_verify")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RSA Cipher"))
        self.titleLabel.setText(_translate("MainWindow", "RSA CIPHER"))
        self.btn_gen_keys.setText(_translate("MainWindow", "Generate Keys"))
        self.lbl_plain.setText(_translate("MainWindow", "Plain Text:"))
        self.lbl_cipher.setText(_translate("MainWindow", "CipherText:"))
        self.btn_encrypt.setText(_translate("MainWindow", "Encrypt"))
        self.btn_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.lbl_info.setText(_translate("MainWindow", "Information:"))
        self.lbl_signature.setText(_translate("MainWindow", "Signature:"))
        self.btn_sign.setText(_translate("MainWindow", "Sign"))
        self.btn_verify.setText(_translate("MainWindow", "Verify"))
