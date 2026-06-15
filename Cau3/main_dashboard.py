import sys
import os
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QLineEdit, QMessageBox, QGridLayout, QGroupBox
)

# Ensure PyQt5 can load platform plugins properly
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

# Add lab-02 to sys.path to reuse classical cipher implementations
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Câu 2")))

from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence.railfence_cipher import RailFenceCipher
from cipher.playfair.playfair_cipher import PlayFairCipher
from cipher.transposition.transposition_cipher import TranspositionCipher

# Stylesheet for premium modern dark mode
DASHBOARD_STYLE = """
    QMainWindow {
        background-color: #1e1e2e;
    }
    QTabWidget::pane {
        border: 1px solid #45475a;
        background-color: #181825;
        border-radius: 8px;
    }
    QTabBar::tab {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-bottom-color: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QTabBar::tab:selected, QTabBar::tab:hover {
        background-color: #181825;
        border-color: #89b4fa;
        color: #89b4fa;
    }
    QLabel {
        color: #cdd6f4;
        font-size: 13px;
        font-weight: bold;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QTextEdit, QLineEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    QTextEdit:focus, QLineEdit:focus {
        border: 1.5px solid #cba6f7;
    }
    QPushButton {
        background-color: #89b4fa;
        color: #11111b;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 13px;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    QPushButton:hover {
        background-color: #b4befe;
    }
    QPushButton:pressed {
        background-color: #313244;
        color: #cdd6f4;
    }
    QGroupBox {
        border: 1px solid #45475a;
        border-radius: 8px;
        margin-top: 15px;
        color: #f5c2e7;
        font-weight: bold;
        font-size: 14px;
        padding: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 5px 0 5px;
    }
"""

class MainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unified Cryptography Suite & Verification Dashboard")
        self.resize(1100, 750)
        self.setStyleSheet(DASHBOARD_STYLE)

        # Initialize classical ciphers
        self.vigenere = VigenereCipher()
        self.railfence = RailFenceCipher()
        self.playfair = PlayFairCipher()
        self.transposition = TranspositionCipher()

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header Title
        header = QLabel("CRYPTOGRAPHY WORKBENCH")
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #cba6f7; margin-bottom: 10px; letter-spacing: 2px;")
        main_layout.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.init_classical_tab()
        self.init_asymmetric_tab()
        self.init_combined_tab()

        main_layout.addWidget(self.tabs)

    # 1. CLASSICAL CIPHERS TAB
    def init_classical_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Dropdown to choose classical cipher
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Select Cipher:"))
        self.cipher_selector = QtWidgets.QComboBox()
        self.cipher_selector.addItems(["Vigenère", "Rail Fence", "Playfair", "Transposition"])
        self.cipher_selector.setStyleSheet("""
            QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.cipher_selector.currentTextChanged.connect(self.on_classical_cipher_changed)
        header_layout.addWidget(self.cipher_selector)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Work area
        grid = QGridLayout()
        grid.setSpacing(15)

        # Labels
        grid.addWidget(QLabel("Plain Text:"), 0, 0)
        grid.addWidget(QLabel("Key:"), 1, 0)
        grid.addWidget(QLabel("Cipher Text:"), 2, 0)

        # Text edits
        self.classical_plain = QTextEdit()
        self.classical_plain.setPlaceholderText("Enter plain text here...")
        self.classical_key = QLineEdit()
        self.classical_key.setPlaceholderText("Enter cryptographic key here...")
        self.classical_cipher = QTextEdit()
        self.classical_cipher.setPlaceholderText("Enter or view cipher text here...")

        grid.addWidget(self.classical_plain, 0, 1)
        grid.addWidget(self.classical_key, 1, 1)
        grid.addWidget(self.classical_cipher, 2, 1)

        layout.addLayout(grid)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_class_encrypt = QPushButton("Encrypt")
        self.btn_class_encrypt.setStyleSheet("background-color: #89b4fa; color: #11111b;")
        self.btn_class_encrypt.clicked.connect(self.encrypt_classical)
        
        self.btn_class_decrypt = QPushButton("Decrypt")
        self.btn_class_decrypt.setStyleSheet("background-color: #f38ba8; color: #11111b;")
        self.btn_class_decrypt.clicked.connect(self.decrypt_classical)

        btn_layout.addWidget(self.btn_class_encrypt)
        btn_layout.addWidget(self.btn_class_decrypt)
        layout.addLayout(btn_layout)

        self.tabs.addTab(tab, "Classical Ciphers")

    def on_classical_cipher_changed(self, cipher_name):
        self.classical_plain.clear()
        self.classical_key.clear()
        self.classical_cipher.clear()
        if cipher_name in ["Rail Fence", "Transposition"]:
            self.classical_key.setPlaceholderText("Enter numeric key (integer)...")
        else:
            self.classical_key.setPlaceholderText("Enter alphabetic key (text)...")

    def encrypt_classical(self):
        cipher = self.cipher_selector.currentText()
        text = self.classical_plain.toPlainText()
        key_str = self.classical_key.text()

        if not text or not key_str:
            QMessageBox.warning(self, "Input Error", "Please fill in both Plain Text and Key fields.")
            return

        try:
            if cipher == "Vigenère":
                result = self.vigenere.vigenere_encrypt(text, key_str)
            elif cipher == "Rail Fence":
                result = self.railfence.rail_fence_encrypt(text, int(key_str))
            elif cipher == "Playfair":
                matrix = self.playfair.create_playfair_matrix(key_str)
                result = self.playfair.playfair_encrypt(text, matrix)
            elif cipher == "Transposition":
                result = self.transposition.encrypt(text, int(key_str))
            self.classical_cipher.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Cryptographic Error", f"Encryption failed: {e}")

    def decrypt_classical(self):
        cipher = self.cipher_selector.currentText()
        text = self.classical_cipher.toPlainText()
        key_str = self.classical_key.text()

        if not text or not key_str:
            QMessageBox.warning(self, "Input Error", "Please fill in both Cipher Text and Key fields.")
            return

        try:
            if cipher == "Vigenère":
                result = self.vigenere.vigenere_decrypt(text, key_str)
            elif cipher == "Rail Fence":
                result = self.railfence.rail_fence_decrypt(text, int(key_str))
            elif cipher == "Playfair":
                matrix = self.playfair.create_playfair_matrix(key_str)
                result = self.playfair.playfair_decrypt(text, matrix)
            elif cipher == "Transposition":
                result = self.transposition.decrypt(text, int(key_str))
            self.classical_plain.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Cryptographic Error", f"Decryption failed: {e}")


    # 2. ASYMMETRIC CIPHERS TAB (RSA & ECC Clients Combined)
    def init_asymmetric_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Left: RSA
        rsa_group = QGroupBox("RSA Cryptosystem")
        rsa_layout = QVBoxLayout(rsa_group)
        rsa_layout.setSpacing(10)
        
        rsa_keys_layout = QHBoxLayout()
        rsa_keys_layout.addWidget(QLabel("RSA Actions:"))
        btn_rsa_gen = QPushButton("Gen RSA Keys")
        btn_rsa_gen.clicked.connect(self.api_rsa_gen)
        rsa_keys_layout.addWidget(btn_rsa_gen)
        rsa_layout.addLayout(rsa_keys_layout)

        rsa_layout.addWidget(QLabel("Plain Text:"))
        self.rsa_plain = QTextEdit()
        rsa_layout.addWidget(self.rsa_plain)

        rsa_layout.addWidget(QLabel("Cipher Text (Hex):"))
        self.rsa_cipher_box = QTextEdit()
        rsa_layout.addWidget(self.rsa_cipher_box)

        rsa_btn_row = QHBoxLayout()
        btn_rsa_enc = QPushButton("Encrypt")
        btn_rsa_enc.clicked.connect(self.api_rsa_encrypt)
        btn_rsa_dec = QPushButton("Decrypt")
        btn_rsa_dec.clicked.connect(self.api_rsa_decrypt)
        rsa_btn_row.addWidget(btn_rsa_enc)
        rsa_btn_row.addWidget(btn_rsa_dec)
        rsa_layout.addLayout(rsa_btn_row)

        # Right: ECC (ECDSA)
        ecc_group = QGroupBox("ECC (ECDSA) Cryptosystem")
        ecc_layout = QVBoxLayout(ecc_group)
        ecc_layout.setSpacing(10)

        ecc_keys_layout = QHBoxLayout()
        ecc_keys_layout.addWidget(QLabel("ECC Actions:"))
        btn_ecc_gen = QPushButton("Gen ECC Keys")
        btn_ecc_gen.clicked.connect(self.api_ecc_gen)
        ecc_keys_layout.addWidget(btn_ecc_gen)
        ecc_layout.addLayout(ecc_keys_layout)

        ecc_layout.addWidget(QLabel("Message Content:"))
        self.ecc_msg = QTextEdit()
        ecc_layout.addWidget(self.ecc_msg)

        ecc_layout.addWidget(QLabel("Signature (Hex):"))
        self.ecc_sig = QTextEdit()
        ecc_layout.addWidget(self.ecc_sig)

        ecc_btn_row = QHBoxLayout()
        btn_ecc_sign = QPushButton("Sign")
        btn_ecc_sign.clicked.connect(self.api_ecc_sign)
        btn_ecc_verify = QPushButton("Verify")
        btn_ecc_verify.clicked.connect(self.api_ecc_verify)
        ecc_btn_row.addWidget(btn_ecc_sign)
        ecc_btn_row.addWidget(btn_ecc_verify)
        ecc_layout.addLayout(ecc_btn_row)

        layout.addWidget(rsa_group, 1)
        layout.addWidget(ecc_group, 1)
        self.tabs.addTab(tab, "Asymmetric Ciphers")

    # API Helpers for RSA
    def api_rsa_gen(self):
        try:
            r = requests.get("http://127.0.0.1:5000/api/rsa/generate_keys")
            if r.status_code == 200:
                QMessageBox.information(self, "RSA Keys", r.json()["message"])
            else:
                QMessageBox.critical(self, "API Error", "Could not generate RSA keys.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Is Flask API running on port 5000? {e}")

    def api_rsa_encrypt(self):
        try:
            r = requests.post("http://127.0.0.1:5000/api/rsa/encrypt", json={
                "message": self.rsa_plain.toPlainText(),
                "key_type": "public"
            })
            if r.status_code == 200:
                self.rsa_cipher_box.setText(r.json()["encrypted_message"])
                QMessageBox.information(self, "Success", "Message encrypted successfully.")
            else:
                QMessageBox.critical(self, "API Error", "Encryption failed.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def api_rsa_decrypt(self):
        try:
            r = requests.post("http://127.0.0.1:5000/api/rsa/decrypt", json={
                "ciphertext": self.rsa_cipher_box.toPlainText(),
                "key_type": "private"
            })
            if r.status_code == 200:
                self.rsa_plain.setText(r.json()["decrypted_message"])
                QMessageBox.information(self, "Success", "Message decrypted successfully.")
            else:
                QMessageBox.critical(self, "API Error", "Decryption failed.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    # API Helpers for ECC
    def api_ecc_gen(self):
        try:
            r = requests.get("http://127.0.0.1:5000/api/ecc/generate_keys")
            if r.status_code == 200:
                QMessageBox.information(self, "ECC Keys", r.json()["message"])
            else:
                QMessageBox.critical(self, "API Error", "Could not generate ECC keys.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def api_ecc_sign(self):
        try:
            r = requests.post("http://127.0.0.1:5000/api/ecc/sign", json={
                "message": self.ecc_msg.toPlainText()
            })
            if r.status_code == 200:
                self.ecc_sig.setText(r.json()["signature"])
                QMessageBox.information(self, "Success", "Message signed successfully.")
            else:
                QMessageBox.critical(self, "API Error", "Signing failed.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def api_ecc_verify(self):
        try:
            r = requests.post("http://127.0.0.1:5000/api/ecc/verify", json={
                "message": self.ecc_msg.toPlainText(),
                "signature": self.ecc_sig.toPlainText()
            })
            if r.status_code == 200:
                if r.json()["is_verified"]:
                    QMessageBox.information(self, "Verification", "Signature is VALID.")
                else:
                    QMessageBox.warning(self, "Verification", "Signature is INVALID.")
            else:
                QMessageBox.critical(self, "API Error", "Verification call failed.")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))


    # 3. COMBINED SIGNATURE VERIFICATION TAB (Câu 02)
    def init_combined_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        layout.addWidget(QLabel("Unified Message to Sign (Joint RSA & ECC):"))
        self.combined_msg = QTextEdit()
        self.combined_msg.setPlaceholderText("Enter the message content that both RSA and ECC will sign...")
        layout.addWidget(self.combined_msg)

        # Grid containing RSA and ECC signature boxes side-by-side
        sig_grid = QGridLayout()
        
        rsa_box = QGroupBox("RSA Digital Signature")
        rsa_box_lay = QVBoxLayout(rsa_box)
        self.combined_rsa_sig = QTextEdit()
        self.combined_rsa_sig.setPlaceholderText("RSA Signature (Hex) will appear here...")
        rsa_box_lay.addWidget(self.combined_rsa_sig)
        
        ecc_box = QGroupBox("ECC Digital Signature")
        ecc_box_lay = QVBoxLayout(ecc_box)
        self.combined_ecc_sig = QTextEdit()
        self.combined_ecc_sig.setPlaceholderText("ECC Signature (Hex) will appear here...")
        ecc_box_lay.addWidget(self.combined_ecc_sig)

        sig_grid.addWidget(rsa_box, 0, 0)
        sig_grid.addWidget(ecc_box, 0, 1)
        layout.addLayout(sig_grid)

        # Control Row
        ctrl_row = QHBoxLayout()
        btn_joint_gen = QPushButton("Generate All Keys")
        btn_joint_gen.setStyleSheet("background-color: #fab387; color: #11111b;")
        btn_joint_gen.clicked.connect(self.joint_generate_keys)
        
        btn_joint_sign = QPushButton("Sign Message (RSA & ECC)")
        btn_joint_sign.setStyleSheet("background-color: #cba6f7; color: #11111b;")
        btn_joint_sign.clicked.connect(self.joint_sign_message)
        
        btn_joint_verify = QPushButton("Verify Both Signatures")
        btn_joint_verify.setStyleSheet("background-color: #a6e3a1; color: #11111b;")
        btn_joint_verify.clicked.connect(self.joint_verify_signatures)

        ctrl_row.addWidget(btn_joint_gen)
        ctrl_row.addWidget(btn_joint_sign)
        ctrl_row.addWidget(btn_joint_verify)
        layout.addLayout(ctrl_row)

        self.tabs.addTab(tab, "Combined Signature Panel")

    def joint_generate_keys(self):
        try:
            r1 = requests.get("http://127.0.0.1:5000/api/rsa/generate_keys")
            r2 = requests.get("http://127.0.0.1:5000/api/ecc/generate_keys")
            if r1.status_code == 200 and r2.status_code == 200:
                QMessageBox.information(self, "Key Generation", "RSA and ECC keys generated successfully!")
            else:
                QMessageBox.critical(self, "Key Generation", "Failed to generate keys.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {e}")

    def joint_sign_message(self):
        msg = self.combined_msg.toPlainText()
        if not msg:
            QMessageBox.warning(self, "Input Error", "Please write a message first.")
            return

        try:
            # Sign with RSA
            r1 = requests.post("http://127.0.0.1:5000/api/rsa/sign", json={"message": msg})
            # Sign with ECC
            r2 = requests.post("http://127.0.0.1:5000/api/ecc/sign", json={"message": msg})

            if r1.status_code == 200 and r2.status_code == 200:
                self.combined_rsa_sig.setText(r1.json()["signature"])
                self.combined_ecc_sig.setText(r2.json()["signature"])
                QMessageBox.information(self, "Signing Status", "Successfully generated signatures for both RSA and ECC!")
            else:
                QMessageBox.critical(self, "Signing Status", "Failed to sign message.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {e}")

    def joint_verify_signatures(self):
        msg = self.combined_msg.toPlainText()
        rsa_sig = self.combined_rsa_sig.toPlainText()
        ecc_sig = self.combined_ecc_sig.toPlainText()

        if not msg or not rsa_sig or not ecc_sig:
            QMessageBox.warning(self, "Input Error", "Please ensure message and signatures are filled in.")
            return

        try:
            r1 = requests.post("http://127.0.0.1:5000/api/rsa/verify", json={"message": msg, "signature": rsa_sig})
            r2 = requests.post("http://127.0.0.1:5000/api/ecc/verify", json={"message": msg, "signature": ecc_sig})

            if r1.status_code == 200 and r2.status_code == 200:
                rsa_valid = r1.json()["is_verified"]
                ecc_valid = r2.json()["is_verified"]

                status_msg = f"RSA Signature Status: {'VALID' if rsa_valid else 'INVALID'}\n"
                status_msg += f"ECC Signature Status: {'VALID' if ecc_valid else 'INVALID'}"
                
                if rsa_valid and ecc_valid:
                    QMessageBox.information(self, "Verification Results", status_msg)
                else:
                    QMessageBox.warning(self, "Verification Results", status_msg)
            else:
                QMessageBox.critical(self, "Verification", "Failed to call verification APIs.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDashboard()
    window.show()
    sys.exit(app.exec_())
