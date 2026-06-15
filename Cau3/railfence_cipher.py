import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow

# Ensure PyQt5 can load platform plugins properly
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms"

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect buttons
        self.ui.btn_clear_all.clicked.connect(self.clear_all)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_visualize.clicked.connect(self.visualize_matrix)
        self.ui.btn_reset.clicked.connect(self.reset_matrix)
        
        # Initialize default Key to 3 for easier user experience
        self.ui.txt_key.setPlainText("3")

    def clear_all(self):
        self.ui.txt_plain_text.clear()
        self.ui.txt_cipher_text.clear()
        self.ui.txt_key.clear()
        self.ui.txt_matrix_representation.clear()
        QMessageBox.information(self, "Clear Fields", "All fields have been cleared.")

    def reset_matrix(self):
        self.ui.txt_matrix_representation.clear()
        QMessageBox.information(self, "Reset", "Matrix representation cleared.")

    def get_rails_key(self):
        key_str = self.ui.txt_key.toPlainText().strip()
        if not key_str:
            QMessageBox.warning(self, "Validation Error", "Please enter the Key (Number of Rails).")
            return None
        try:
            rails = int(key_str)
            if rails < 2:
                QMessageBox.warning(self, "Validation Error", "Key (Number of Rails) must be at least 2.")
                return None
            return rails
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Key (Number of Rails) must be an integer.")
            return None

    def call_api_encrypt(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        if not plain_text.strip():
            QMessageBox.warning(self, "Input Error", "Please enter Plain Text to encrypt.")
            return
            
        key = self.get_rails_key()
        if key is None:
            return

        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        payload = {
            "plain_text": plain_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    QMessageBox.warning(self, "Error", data["error"])
                else:
                    self.ui.txt_cipher_text.setText(data["encrypted_text"])
                    # Automatically visualize matrix
                    self.show_matrix_viz(plain_text, key)
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", f"Error from API: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", f"Connection failed: {e}\nIs the API server running?")

    def call_api_decrypt(self):
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        if not cipher_text.strip():
            QMessageBox.warning(self, "Input Error", "Please enter CipherText to decrypt.")
            return
            
        key = self.get_rails_key()
        if key is None:
            return

        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        payload = {
            "cipher_text": cipher_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    QMessageBox.warning(self, "Error", data["error"])
                else:
                    decrypted_text = data["decrypted_text"]
                    self.ui.txt_plain_text.setText(decrypted_text)
                    # Automatically visualize matrix
                    self.show_matrix_viz(decrypted_text, key)
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()
            else:
                QMessageBox.critical(self, "API Error", f"Error from API: Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", f"Connection failed: {e}\nIs the API server running?")

    def show_matrix_viz(self, text, rails):
        if not text or rails < 2:
            return
        
        # Generate visual zigzag matrix representation
        matrix = [["." for _ in range(len(text))] for _ in range(rails)]
        rail_idx = 0
        direction = 1
        for col, char in enumerate(text):
            matrix[rail_idx][col] = char
            if rail_idx == 0:
                direction = 1
            elif rail_idx == rails - 1:
                direction = -1
            rail_idx += direction
            
        lines = []
        for r in range(rails):
            lines.append("   ".join(matrix[r])) # add some spacing for better visuals
            
        self.ui.txt_matrix_representation.setText("\n".join(lines))

    def visualize_matrix(self):
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.get_rails_key()
        if key is None:
            return
        if not plain_text.strip():
            # If no plain text, try cipher text
            cipher_text = self.ui.txt_cipher_text.toPlainText()
            if cipher_text.strip():
                # We show message that we visualize the cipher text's pattern or decrypted text
                plain_text = cipher_text
            else:
                QMessageBox.warning(self, "Input Error", "Please enter Plain Text or Cipher Text to visualize matrix pattern.")
                return
        
        self.show_matrix_viz(plain_text, key)
        QMessageBox.information(self, "Visualization", "Generated Rail Fence Zigzag Matrix Pattern successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())
