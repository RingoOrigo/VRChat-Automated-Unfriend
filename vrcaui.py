import sys, vrcau

from vrchatapi.exceptions import UnauthorizedException
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

class UIHandler:
    def __init__ (self):
        self.app = QApplication(sys.argv)
        self.loader = QUiLoader()
        login_ui_file = QFile("interface/login.ui")
        self.window = self.loader.load(login_ui_file)
        self.client = vrcau.VRCAU()
        self.currentPopup = None

    def showLogin (self):
        self.window.show()

        login_button = self.window.loginButton
        login_button.clicked.connect(lambda: self.setLoginInfo())

        # Ready the error text field
        self.window.errorField.setVisible(False)
        
        # Ensure that the destroy function is called when the window closes.
        self.app.setQuitOnLastWindowClosed(False)
        self.app.lastWindowClosed.connect(self.client.destroy)


        sys.exit(self.app.exec())

    def setLoginInfo (self):
        self.client.username = self.window.usernameField.text().strip()
        self.client.password = self.window.passwordField.text().strip()
        self.client.save_login = self.window.rememberMeBox.isChecked()

        # Proceed to login process.
        try:
            self.client.login()
        except vrcau.MFARequirementError as e:
            self.showMFA()
        except vrcau.LoginError:
            self.window.errorField.setVisible(True)

    def setAuthInfo (self):
        self.currentPopup.close()
        self.client.auth_code = self.currentPopup.mfaField.text().strip()

        try:
            self.client.authenticate()
        except UnauthorizedException as e:
            if e.status == 401:
                self.showMFA(failed_attempt=True)
            else:
                print("Error verifying 2FA code")

    def showMFA (self, failed_attempt = False):
        """Prompt for 2FA code and continue the login process."""

        mfa_ui_file = QFile("interface/mfa.ui")
        self.currentPopup = self.loader.load(mfa_ui_file)
        self.currentPopup.show()

        if not failed_attempt:
            self.currentPopup.errorField.setVisible(False)

        button = self.currentPopup.submitButton
        button.clicked.connect(lambda: self.setAuthInfo())

# if __name__ == "__main__":

#     # Initialize the login screen.
#     app = QApplication(sys.argv)
#     ui_file = QFile("interface/login.ui")
#     loader = QUiLoader()
#     ui_file.close()

#     # Show the login screen.
#     window = loader.load(ui_file)
#     window.show()
    
#     # Connect the login button to the info retrieval function.
#     login_button = window.loginButton
#     login_button.clicked.connect(lambda: getLoginInfo(window))

#     # Ready the error text field
#     window.errorField.setVisible(False)

#     sys.exit(app.exec())