import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_GenerateKeys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_Encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_Decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_Sign.clicked.connect(self.call_api_sign)
        self.ui.btn_Verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(data["message"])
                    msg.exec_()
                else:
                    print("Error: 'message' key not found in API response")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Failed to generate keys: Invalid response format")
                    msg.exec_()
            else:
                print(f"ERROR WHILE CALLING API: Status code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Failed to generate keys: API error")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error connecting to API: {str(e)}")
            msg.exec_()

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_PlainText.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "encrypted_message" in data:
                    self.ui.txt_CipherText.setText(data["encrypted_message"])
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()
                else:
                    print("Error: 'encrypted_message' key not found in API response")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Encryption failed: Invalid response format")
                    msg.exec_()
            else:
                print(f"ERROR WHILE CALLING API: Status code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Encryption failed: API error")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error connecting to API: {str(e)}")
            msg.exec_()

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_CipherText.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("API response:", data)
                decrypted_message = None
                if "decrypted_message" in data:
                    decrypted_message = data["decrypted_message"]
                elif "message" in data:
                    decrypted_message = data["message"]
                elif "plaintext" in data:
                    decrypted_message = data["plaintext"]
                elif "tin nhắn đã giải mã" in data:
                    decrypted_message = data["tin nhắn đã giải mã"]
                
                if decrypted_message:
                    self.ui.txt_PlainText.setText(decrypted_message)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()
                else:
                    print("Error: No recognizable decrypted message key found in API response")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Decryption failed: No decrypted message in response")
                    msg.exec_()
            else:
                print(f"ERROR WHILE CALLING API: Status code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Decryption failed: API error")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error connecting to API: {str(e)}")
            msg.exec_()

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_Information.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("API response:", data)
                signature = None
                if "signature" in data:
                    signature = data["signature"]
                elif "chữ ký" in data:
                    signature = data["chữ ký"]
                
                if signature:
                    self.ui.txt_Signature.setText(signature)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("SIGNED SUCCESSFULLY")
                    msg.exec_()
                else:
                    print("Error: No recognizable signature key found in API response")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Signing failed: No signature in response")
                    msg.exec_()
            else:
                print(f"ERROR WHILE CALLING API: Status code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Signing failed: API error")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error connecting to API: {str(e)}")
            msg.exec_()

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_Information.toPlainText(),
            "signature": self.ui.txt_Signature.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("API response:", data)
                is_verified = None
                if "is_verified" in data:
                    is_verified = data["is_verified"]
                elif "được_xác minh" in data:  # Sửa key để khớp với API
                    is_verified = data["được_xác minh"]
                
                if is_verified is not None:
                    if is_verified:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Verified Successfully")
                        msg.exec_()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Verified FAIL")
                        msg.exec_()
                else:
                    print("Error: No recognizable verification key found in API response")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Verification failed: Invalid response format")
                    msg.exec_()
            else:
                print(f"ERROR WHILE CALLING API: Status code {response.status_code}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Verification failed: API error")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error connecting to API: {str(e)}")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())